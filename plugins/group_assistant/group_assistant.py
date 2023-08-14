# encoding:utf-8
import json
import os

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from common.log import logger
from plugins import *
from config import conf


@plugins.register(
    name="group_assistant",
    desire_priority=-1,
    hidden=False,
    desc="group_assistant",
    version="0.1",
    author="chazzjimel",
)
class GroupAssistant(Plugin):
    def __init__(self):
        super().__init__()
        try:
            # 获取当前文件的目录
            curdir = os.path.dirname(__file__)
            # 配置文件的路径
            config_path = os.path.join(curdir, "config.json")
            if_ntchat = conf().get("channel_type", "")
            # 如果配置文件不存在
            if not os.path.exists(config_path):
                # 输出日志信息，配置文件不存在，将使用模板
                logger.error('[GroupAssistant] 配置文件不存在，无法启动插件')
                return
            elif if_ntchat != "ntchat":
                logger.error('[GroupAssistant] 不是ntchat通道，无法启动插件')
                return
                # 打开并读取配置文件
            with open(config_path, "r", encoding="utf-8") as f:
                # 加载 JSON 文件
                self.config = json.load(f)
            # 设置事件处理函数
            self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
            # 输出日志信息，表示插件已初始化
            logger.info("[GroupAssistant] inited")
        except Exception as e:  # 捕获所有的异常
            logger.warn("[RP] init failed." + str(e))
            # 抛出异常，结束程序
            raise e

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        elif e_context["context"]["isgroup"]:
            return

        content = e_context["context"].content
        logger.debug("[GroupAssistant] on_handle_context. content: %s" % content)
        reply = Reply()

        if "进群" in content:
            # 使用split函数，以"："或者":"为分隔符，将content分割成两部分
            parts = None
            if "：" in content:
                parts = content.split("：")
            elif ":" in content:
                parts = content.split(":")
            else:
                reply.type = ReplyType.TEXT
                reply.content = "进群指令有误，请使用：分隔！"

            # 如果分割后的列表长度大于1，说明"："或":"存在于content中
            if len(parts) > 1:
                # 获取"："后面的部分，即群名，使用strip函数去除可能存在的首尾空格
                group_name = parts[1].strip()
                # 从self.config中获取对应的值
                group_id = self.config.get(group_name)
                if group_id:
                    reply.type = ReplyType.InviteRoom
                    reply.content = group_id
                else:
                    reply.type = ReplyType.TEXT
                    reply.content = "没有该群聊信息，请检查！"
            else:
                reply.type = ReplyType.TEXT
                reply.content = "没有输入群名，请检查！"
        else:
            logger.info("[GroupAssistant]此消息不是进群请求···")
            return
        e_context["reply"] = reply
        e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑

    def get_help_text(self, **kwargs):
        help_text = "邀请进群插件"
        return help_text
