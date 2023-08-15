import openai
import requests
import plugins

from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from plugins import *
from common.log import logger
from plugins.newgpt_turbo.lib import function as fun, get_stock_info as stock, search_google as google
from datetime import datetime
from bridge.bridge import Bridge


def create_channel_object():
    channel_type = conf().get("channel_type")
    if channel_type == 'wework':
        from channel.wework.wework_channel import WeworkChannel
        return WeworkChannel()
    elif channel_type == 'ntchat':
        from channel.wechatnt.ntchat_channel import NtchatChannel
        return NtchatChannel()
    elif channel_type == 'weworktop':
        from channel.weworktop.weworktop_channel import WeworkTopChannel
        return WeworkTopChannel()
    else:
        from channel.wechatnt.ntchat_channel import NtchatChannel
        return NtchatChannel()


def up_fastgpt(fastgpt_url, fastgpt_api_key, fast_kbid_list, a, q, receiver):
    url = fastgpt_url
    headers = {
        'apikey': fastgpt_api_key,
        'Content-Type': 'application/json',
    }

    kbId = fast_kbid_list[receiver]
    data = {
        "kbId": kbId,
        "mode": "index",
        "prompt": "",
        "data": [
            {
                "a": a,
                "q": q
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        logger.debug(f"提交的数据体：{data}")
        logger.debug(f"保存到知识库响应：{response.text}")
    except requests.exceptions.RequestException as e:
        # 打印错误信息
        logger.error(f"请求失败：{e}")


@plugins.register(name="NewGpt_Turbo", desc="GPT函数调用，极速联网", desire_priority=990, version="0.1",
                  author="chazzjimel", )
class NewGpt(Plugin):
    def __init__(self):
        super().__init__()
        curdir = os.path.dirname(__file__)
        config_path = os.path.join(curdir, "config.json")
        functions_path = os.path.join(curdir, "lib", "functions.json")
        logger.info(f"[newgpt_turbo] current directory: {curdir}")
        logger.info(f"加载配置文件: {config_path}")
        if not os.path.exists(config_path):
            logger.info('[newgpt_turbo] 配置文件不存在，将使用config.json.template模板')
            config_path = os.path.join(curdir, "config.json.template")
            logger.info(f"[newgpt_turbo] config template path: {config_path}")
        try:
            with open(functions_path, 'r', encoding="utf-8") as f:
                functions = json.load(f)
                self.functions = functions
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                logger.debug(f"[newgpt_turbo] config content: {config}")
                self.openai_api_key = config.get("open_ai_api_key")
                self.openai_api_base = config.get("open_ai_api_base", "https://api.openai.com/v1")
                self.alapi_key = config["alapi_key"]
                self.bing_subscription_key = config["bing_subscription_key"]
                self.google_api_key = config["google_api_key"]
                self.google_cx_id = config["google_cx_id"]
                self.functions_openai_model = config["functions_openai_model"]
                self.assistant_openai_model = config["assistant_openai_model"]
                self.app_key = config["app_key"]
                self.app_sign = config["app_sign"]
                self.temperature = config.get("temperature", 0.9)
                self.max_tokens = config.get("max_tokens", 1000)
                self.google_base_url = config.get("google_base_url", "https://www.googleapis.com/customsearch/v1?")
                self.comapp = create_channel_object()
                self.prompt = config["prompt"]
                self.fastgpt = config.get("fastgpt", False)
                self.fastgpt_url = config.get("fastgpt_url", "")
                self.fastgpt_api_key = config.get("fastgpt_api_key", "")
                self.fast_kbid_list = config.get("fast_kbid_list", {})
                self.card_wxid = config.get("card_wxid", "")
                self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
                logger.info("[newgpt_turbo] inited")
        except Exception as e:
            if isinstance(e, FileNotFoundError):
                logger.warn(f"[newgpt_turbo] init failed, config.json not found.")
            else:
                logger.warn("[newgpt_turbo] init failed." + str(e))
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [ContextType.TEXT]:
            return
        reply = Reply()  # 创建一个回复对象
        reply.type = ReplyType.TEXT
        context = e_context['context'].content[:]
        logger.info("newgpt_turbo query=%s" % context)
        all_sessions = Bridge().get_bot("chat").sessions
        session = all_sessions.session_query(context, e_context["context"]["session_id"], add_to_history=False)
        logger.debug("session.messages:%s" % session.messages)
        if len(session.messages) > 2:
            input_messages = session.messages[-2:]
        else:
            input_messages = session.messages[-1:]
        promt1 = {"role": "system", "content": "请判断用户输入是否需要调用函数，如果不需要直接返回不需要调用函数，不用你自己进行解答！"}
        promt2 = {"role": "user", "content": context}
        input_messages.extend([promt1, promt2])
        logger.debug("input_messages:%s" % input_messages)
        conversation_output = self.run_conversation(input_messages, e_context)
        if conversation_output is not None:
            _reply = conversation_output
            logger.debug("conversation_output:%s" % conversation_output)
            all_sessions.session_query(context, e_context["context"]["session_id"])
            all_sessions.session_reply(_reply, e_context["context"]["session_id"])
            reply.content = _reply
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS
            return
        else:
            return

    def run_conversation(self, input_messages, e_context: EventContext):
        global function_response
        content = e_context['context'].content[:]
        messages = []
        logger.debug(f"User input: {input_messages}")  # 用户输入
        openai.api_key = self.openai_api_key
        openai.api_base = self.openai_api_base
        response = openai.ChatCompletion.create(
            model=self.functions_openai_model,
            messages=input_messages,
            functions=self.functions,
            function_call="auto",
        )

        message = response["choices"][0]["message"]

        # 检查模型是否希望调用函数
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            logger.debug(f"Function call: {function_name}")  # 打印函数调用
            logger.debug(f"message={message}")
            # 处理各种可能的函数调用，执行函数并获取函数的返回结果
            if function_name == "get_weather":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数
                function_response = fun.get_weather(appkey=self.app_key, sign=self.app_sign,
                                                    cityNm=function_args.get("cityNm", "未指定地点"))
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_morning_news":
                function_response = fun.get_morning_news(api_key=self.alapi_key)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_hotlist":
                function_args_str = message["function_call"].get("arguments", "{}")
                function_args = json.loads(function_args_str)  # 使用 json.loads 将字符串转换为字典
                hotlist_type = function_args.get("type", "未指定类型")
                function_response = fun.get_hotlist(api_key=self.alapi_key, type=hotlist_type)
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "search":
                function_args_str = message["function_call"].get("arguments", "{}")
                function_args = json.loads(function_args_str)  # 使用 json.loads 将字符串转换为字典
                search_query = function_args.get("query", "未指定关键词")
                search_count = function_args.get("count", 1)
                if "必应" in content or "newbing" in content.lower():
                    com_reply = Reply()
                    com_reply.type = ReplyType.TEXT
                    context = e_context['context']
                    if context.kwargs.get('isgroup'):
                        msg = context.kwargs.get('msg')  # 这是WechatMessage实例
                        nickname = msg.actual_user_nickname  # 获取nickname
                        com_reply.content = "@{name}\n☑️正在给您实时联网必应搜索\n⏳整理深度数据需要时间，请耐心等待...".format(
                            name=nickname)
                    else:
                        com_reply.content = "☑️正在给您实时联网必应搜索\n⏳整理深度数据需要时间，请耐心等待..."
                    if self.comapp is not None:
                        self.comapp.send(com_reply, e_context['context'])
                    function_response = fun.search_bing(subscription_key=self.bing_subscription_key, query=search_query,
                                                        count=int(search_count))
                    function_response = json.dumps(function_response, ensure_ascii=False)
                    logger.debug(f"Function response: {function_response}")  # 打印函数响应
                elif "谷歌" in content or "搜索" in content or "google" in content.lower():
                    com_reply = Reply()
                    com_reply.type = ReplyType.TEXT
                    context = e_context['context']
                    if context.kwargs.get('isgroup'):
                        msg = context.kwargs.get('msg')  # 这是WechatMessage实例
                        nickname = msg.actual_user_nickname  # 获取nickname
                        com_reply.content = "@{name}\n☑️正在给您实时联网谷歌搜索\n⏳整理深度数据需要几分钟，请您耐心等待...".format(
                            name=nickname)
                    else:
                        com_reply.content = "☑️正在给您实时联网谷歌搜索\n⏳整理深度数据需要几分钟，请您耐心等待..."
                    if self.comapp is not None:
                        self.comapp.send(com_reply, e_context['context'])
                    function_response = google.search_google(search_terms=search_query, base_url=self.google_base_url,
                                                             iterations=1, count=1,
                                                             api_key=self.google_api_key, cx_id=self.google_cx_id,
                                                             model=self.assistant_openai_model)
                    logger.debug(f"google.search_google url: {self.google_base_url}")
                    function_response = json.dumps(function_response, ensure_ascii=False)
                    logger.debug(f"Function response: {function_response}")  # 打印函数响应
                else:
                    return None
            elif function_name == "get_oil_price":
                function_response = fun.get_oil_price(api_key=self.alapi_key)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_Constellation_analysis":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数

                function_response = fun.get_Constellation_analysis(api_key=self.alapi_key,
                                                                   star=function_args.get("star", "未指定星座"),
                                                                   )
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "music_search":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数

                function_response = fun.music_search(api_key=self.alapi_key,
                                                     keyword=function_args.get("keyword", "未指定音乐"),
                                                     )
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_datetime":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数
                city = function_args.get("city_en", "未指定城市")  # 如果没有指定城市，将默认查询北京
                function_response = fun.get_datetime(appkey=self.app_key, sign=self.app_sign, city_en=city)
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_url":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数
                url = function_args.get("url", "未指定URL")
                function_response = fun.get_url(url=url)
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_stock_info":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数
                stock_names = function_args.get("stock_names", "未指定股票信息")
                function_response = stock.get_stock_info(stock_names=stock_names, appkey=self.app_key,
                                                         sign=self.app_sign)
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_video_url":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数
                url = function_args.get("url", "无URL")
                viedo_url = fun.get_video_url(api_key=self.alapi_key, target_url=url)
                if viedo_url:
                    logger.debug(f"viedo_url: {viedo_url}")
                    reply = Reply()  # 创建一个回复对象
                    reply.type = ReplyType.VIDEO_URL
                    reply.content = viedo_url
                    e_context["reply"] = reply
                    e_context.action = EventAction.BREAK_PASS
                    return
                else:
                    reply = Reply()  # 创建一个回复对象
                    reply.type = ReplyType.TEXT
                    reply.content = "抱歉，解析失败了·······"
                    e_context["reply"] = reply
                    e_context.action = EventAction.BREAK_PASS
                    return
            elif function_name == "search_bing_news":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数
                search_query = function_args.get("query", "未指定关键词")
                search_count = function_args.get("count", 10)
                function_response = fun.search_bing_news(count=search_count,
                                                         subscription_key=self.bing_subscription_key,
                                                         query=search_query, )
                function_response = json.dumps(function_response, ensure_ascii=False)
                logger.debug(f"Function response: {function_response}")  # 打印函数响应
            elif function_name == "get_contact_information":
                if not self.card_wxid:
                    return
                else:
                    reply = Reply()
                    reply.type = ReplyType.CARD
                    reply.content = self.card_wxid
                    e_context["reply"] = reply
                    e_context.action = EventAction.BREAK_PASS
                    return
            elif function_name == "time_task_assistant":
                function_args = json.loads(message["function_call"].get("arguments", "{}"))
                logger.debug(f"Function arguments: {function_args}")  # 打印函数参数
                cycle = function_args.get("cycle")
                time = function_args.get("time")
                event_ = function_args.get("event")
                function_message = "$time" + " " + cycle + " " + time + " " + event_
                e_context["context"].content = function_message
                e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑
                return
            else:
                return

            msg: ChatMessage = e_context["context"]["msg"]
            current_date = datetime.now().strftime("%Y年%m月%d日%H时%M分")
            if e_context["context"]["isgroup"]:
                prompt = self.prompt.format(time=current_date, bot_name=msg.to_user_nickname,
                                            name=msg.actual_user_nickname, content=content,
                                            function_response=function_response)
            else:
                prompt = self.prompt.format(time=current_date, bot_name=msg.to_user_nickname,
                                            name=msg.from_user_nickname, content=content,
                                            function_response=function_response)
            # 将函数的返回结果发送给第二个模型
            logger.debug(f"prompt :" + prompt)
            logger.debug("messages: %s", [{"role": "system", "content": prompt}])
            second_response = openai.ChatCompletion.create(
                model=self.assistant_openai_model,
                messages=[
                    {"role": "system", "content": prompt},
                ],
                temperature=float(self.temperature),
                max_tokens=int(self.max_tokens)
            )

            logger.debug(f"Second response: {second_response['choices'][0]['message']['content']}")  # 打印第二次的响应
            messages.append(second_response["choices"][0]["message"])
            if self.fastgpt:
                context = e_context['context']
                if context.kwargs.get('isgroup'):
                    now = datetime.now()
                    date_string = now.strftime("%Y年%m月%d日%H时%M分")
                    fast_q = date_string + " " + msg.actual_user_nickname + ":" + content
                    up_fastgpt(fastgpt_url=self.fastgpt_url, fastgpt_api_key=self.fastgpt_api_key,
                               fast_kbid_list=self.fast_kbid_list,
                               a=second_response['choices'][0]['message']['content'], q=fast_q,
                               receiver=context.kwargs["receiver"])
                else:
                    logger.debug("非群聊信息")
            else:
                logger.debug("未开启知识库存储")

            return second_response['choices'][0]['message']['content']




        else:
            # 如果模型不希望调用函数，直接打印其响应
            logger.info("模型响应无函数调用，跳过处理")  # 打印模型的响应
            return

    def get_help_text(self, verbose=False, **kwargs):
        # 初始化帮助文本，说明利用 midjourney api 来画图
        help_text = "\n🔥GPT函数调用，极速联网，语境如需联网且有功能支持，则会直接联网获取实时信息\n"
        # 如果不需要详细说明，则直接返回帮助文本
        if not verbose:
            return help_text
        # 否则，添加详细的使用方法到帮助文本中
        help_text = "newgpt_turbo，极速联网无需特殊指令，前置识别\n🔎谷歌搜索、🔎新闻搜索\n🗞每日早报、☀全球天气\n⌚实时时间、⛽全国油价\n🌌星座运势、🎵音乐（网易云）\n🔥各类热榜信息、📹短视频解析等"
        # 返回帮助文本
        return help_text
