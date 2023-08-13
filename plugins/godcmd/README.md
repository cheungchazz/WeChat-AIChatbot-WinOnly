## 插件说明

原项目地址：[`godcmd`](https://github.com/zhayujie/chatgpt-on-wechat/tree/master/plugins/godcmd)，指令插件

添加#debug开和关，方便调试

添加授权码生成和删除

本项目仅作存储用

## 插件使用

将`config.json.template`复制为`config.json`，并修改其中`password`的值为口令。

如果没有设置命令，在命令行日志中会打印出本次的临时口令，请注意观察，打印格式如下。

```
[INFO][2023-04-06 23:53:47][godcmd.py:165] - [Godcmd] 因未设置口令，本次的临时口令为0971。
```

在私聊中可使用`#auth`指令，输入口令进行管理员认证。更多详细指令请输入`#help`查看帮助文档：

`#auth <口令>` - 管理员认证，仅可在私聊时认证。
`#help` - 输出帮助文档，**是否是管理员**和是否是在群聊中会影响帮助文档的输出内容。
