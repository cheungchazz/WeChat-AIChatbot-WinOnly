# encoding:utf-8

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from channel.chat_message import ChatMessage
from common.log import logger
from plugins import *


@plugins.register(
    name="Hello",
    desire_priority=-1,
    hidden=True,
    desc="A simple plugin that says hello",
    version="0.1",
    author="lanvent",
)
class Hello(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[Hello] inited")

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type not in [
            ContextType.TEXT,
            ContextType.JOIN_GROUP,
            ContextType.PATPAT,
        ]:
            return

        if e_context["context"].type == ContextType.JOIN_GROUP:
            e_context["context"].type = ContextType.TEXT
            msg: ChatMessage = e_context["context"]["msg"]
            e_context["context"].content = f'请你随机使用一种说话风格说一句与众不同的问候语来欢迎新用户"{msg.actual_user_nickname}"加入了"{msg.other_user_nickname}"群聊，并告知新用户“群聊内禁止打广告、引流和讨论违法违纪的敏感话题以及仅允许对bot进行轻度使用测试”，不用说你使用了什么风格，直接回复内容就行，除了欢迎内容不要说任何多余的话语。'
            e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑
            return

        if e_context["context"].type == ContextType.PATPAT:
            e_context["context"].type = ContextType.TEXT
            msg: ChatMessage = e_context["context"]["msg"]
            if e_context["context"]["isgroup"]:
                e_context["context"].content = f'请你随机使用一种风格和与众不同的玩笑跟"{msg.actual_user_nickname}"说为什么要拍你的服务器，不用说你使用了什么风格，直接发送玩笑内容开玩笑就行，除了玩笑内容不要说任何多余的话语。'
            else:
                e_context["context"].content = f'请你随机使用一种风格和与众不同的玩笑跟"{msg.from_user_nickname}"说为什么要拍你的服务器，不用说你使用了什么风格，直接发送玩笑内容开玩笑就行，除了玩笑内容不要说任何多余的话语。'
            e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑
            return

        content = e_context["context"].content
        logger.debug("[Hello] on_handle_context. content: %s" % content)
        if content == "Hello":
            reply = Reply()
            reply.type = ReplyType.TEXT
            msg: ChatMessage = e_context["context"]["msg"]
            if e_context["context"]["isgroup"]:
                reply.content = f"Hello, {msg.actual_user_nickname} from {msg.from_user_nickname}"
            else:
                reply.content = f"Hello, {msg.from_user_nickname}"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

        if content == "Hi":
            reply = Reply()
            reply.type = ReplyType.TEXT
            reply.content = "Hi"
            e_context["reply"] = reply
            e_context.action = EventAction.BREAK  # 事件结束，进入默认处理逻辑，一般会覆写reply

        if content == "End":
            # 如果是文本消息"End"，将请求转换成"IMAGE_CREATE"，并将content设置为"The World"
            e_context["context"].type = ContextType.IMAGE_CREATE
            content = "The World"
            e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑

    def get_help_text(self, **kwargs):
        help_text = "输入Hello，我会回复你的名字\n输入End，我会回复你世界的图片\n"
        return help_text
