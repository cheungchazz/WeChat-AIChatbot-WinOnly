# 简介

> **本项目只能在win系统运行**，<u>基于[chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)二改，完全使用了源项目的框架，鸣谢！</u>支持Win平台的PC客户端以及企微客户端，本项目会持续更新，也会逐渐开发插件，一个人开发，勿催，感谢！

项目支持的消息通道及功能如下：

- [x] **WeworkTop**：PC端的企微个人号消息通道（开发中），搭配wework-api软件（进群拿）

  **基础版：**

  - [x] 发送消息：文本/图片/视频/文件/群聊@/链接卡片/GIF
  - [x] 接收消息：All
  - [x] 其他功能：同意加好友请求/创建群/添加好友入群/邀请好友入群/退出群聊
  - [ ] 短板缺陷：无法发送语音条信息

  **付费版：**

  - [x] 全功能

- [x] **Wework**：PC端的企微个人号消息通道，依赖 [ntwork](https://github.com/chazzjimel/ntwork)，限制[WeCom_4.0.8.6027版本](https://dldir1.qq.com/wework/work_weixin/WeCom_4.0.8.6027.exe)，**只能在Win平台运行项目**。

  - [x] 发送消息：文本/图片/视频/文件/群聊@/链接卡片/GIF
  - [x] 接收消息：All
  - [ ] 短板缺陷：无法发送语音条信息

- [x] **Wechat** ：PC端的个微消息通道，依赖 [ntchat项目](https://github.com/billyplus/ntchat) ，最高支持Python310环境版本，限[WeChat3.6.0.18版本](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.6.0.18/WeChatSetup-3.6.0.18.exe)，**只能在Win平台运行项目**。
  - [x] 发送消息：文本/图片/视频/文件/群聊@/链接卡片/GIF
  - [x] 接收消息：All
  - [x] 其他功能：同意加好友请求/创建群/添加好友入群/邀请好友入群/删除群成员/修改群名/修改群公告
  - [ ] 短板缺陷：无法发送语音条信息

# **详细功能列表：**

- [x] 聊天对话：私聊、群聊对话，支持fastgpt、openai、azure、文心一言对话模型通道
- [x] 语音对话：语音消息可选文字或语音回复，支持 azure, openai等语音模型，语音回复仅文件格式，weworktop可实现语音条回复
- [x] 绘画插件：默认openai绘画支持，项目集成MJ绘画插件，待海艺开放API会优先接入做适配
- [x] 联网插件：内置联网插件，通过GPT的函数调用功能实现，目前能用，持续优化中
- [x] 高度定制：依赖fastgpt接口，可实现每个群聊对应不同的应用知识库


# 更新日志

>**2023.08.15：** 更新FastGpt接入逻辑，支持单群单知识库，未配置默认走全局base。
>
>```json
>  {
>      "fast_gpt": true,
>      "fastgpt_list": {
>        "R:108864****63985": "fastgpt-1aps*****pg47-64b16a*******181317",
>        "R:107******373863": "fastgpt-1aps8*****gni1kpg47-64b168*****cd181267"
>    	}
>  }
>```
>
>**2023.08.10：** 添加WeworkTop（企微个人号）消息通道。
>
>**2023.08.08：** 添加Wework（企微个人号）消息通道。
>
>**2023.07.25：** 适添加wechat消息通道，项目兼容[FastGPT](https://github.com/labring/FastGPT) API接口，直接修改open_ai_api_key和open_ai_api_base即可使用。

# 快速开始

## 准备

### 1.运行环境

仅支持Windows 系统同时需安装 `Python`。
> 建议Python版本在 3.7.1~3.10 之间。

**(1) 下载项目代码：**

```bash
git clone https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly
cd chatgpt-on-wechat/
```

**(2) 安装核心依赖 (必选)：**

```bash
pip3 install -r requirements.txt
```

**(3) 拓展依赖 (可选，建议安装)：**

```bash
pip3 install -r requirements-optional.txt
```
> 如果某项依赖安装失败请注释掉对应的行再继续。

其中`tiktoken`要求`python`版本在3.8以上，它用于精确计算会话使用的tokens数量，强烈建议安装。


使用`google`或`baidu`语音识别需安装`ffmpeg`，

默认的`openai`语音识别不需要安装`ffmpeg`。

参考[#415](https://github.com/zhayujie/chatgpt-on-wechat/issues/415)

使用`azure`语音功能需安装依赖，并参考[文档](https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python&tabs=linux%2Cubuntu%2Cdotnet%2Cjre%2Cmaven%2Cnodejs%2Cmac%2Cpypi)的环境要求。
:

```bash
pip3 install azure-cognitiveservices-speech
```

## 配置

配置文件的模板在根目录的`config-template.json`中，需复制该模板创建最终生效的 `config.json` 文件：

```bash
  cp config-template.json config.json
```

然后在`config.json`中填入配置，以下是对默认配置的说明，可根据需要进行自定义修改（请去掉注释）：

```json
# config.json文件内容示例
{
  "open_ai_api_key": "YOUR API KEY",                          # 填入上面创建的 OpenAI API KEY
  "model": "gpt-3.5-turbo",                                   # 模型名称。当use_azure_chatgpt为true时，其名称为Azure上model deployment名称
  "proxy": "",                                                # 代理客户端的ip和端口，国内环境开启代理的需要填写该项，如 "127.0.0.1:7890"
  "single_chat_prefix": ["bot", "@bot"],                      # 私聊时文本需要包含该前缀才能触发机器人回复
  "single_chat_reply_prefix": "[bot] ",                       # 私聊时自动回复的前缀，用于区分真人
  "group_chat_prefix": ["@bot"],                              # 群聊时包含该前缀则会触发机器人回复
  "group_name_white_list": ["ChatGPT测试群", "ChatGPT测试群2"], # 开启自动回复的群名称列表
  "group_chat_in_one_session": ["ChatGPT测试群"],              # 支持会话上下文共享的群名称  
  "image_create_prefix": ["画", "看", "找"],                   # 开启图片回复的前缀
  "conversation_max_tokens": 1000,                            # 支持上下文记忆的最多字符数
  "speech_recognition": false,                                # 是否开启语音识别
  "group_speech_recognition": false,                          # 是否开启群组语音识别
  "use_azure_chatgpt": false,                                 # 是否使用Azure ChatGPT service代替openai ChatGPT service. 当设置为true时需要设置 open_ai_api_base，如 https://xxx.openai.azure.com/
  "azure_deployment_id": "",                                  # 采用Azure ChatGPT时，模型部署名称
  "azure_api_version": "",                                    # 采用Azure ChatGPT时，API版本
  "character_desc": "你是ChatGPT, 一个由OpenAI训练的大型语言模型, 你旨在回答并解决人们的任何问题，并且可以使用多种语言与人交流。",  # 人格描述
  # 订阅消息，公众号和企业微信channel中请填写，当被订阅时会自动回复，可使用特殊占位符。目前支持的占位符有{trigger_prefix}，在程序中它会自动替换成bot的触发词。
  "subscribe_msg": "感谢您的关注！\n这里是ChatGPT，可以自由对话。\n支持语音对话。\n支持图片输出，画字开头的消息将按要求创作图片。\n支持角色扮演和文字冒险等丰富插件。\n输入{trigger_prefix}#help 查看详细指令。",
  "accept_friend": false,                                     # 配置itchat和ntchat自动通过好友请求
  "channel_type": "wx",#通道类型，支持：{wx,wxy,terminal,wechatmp,wechatmp_service,wechatcom_app,ntchat,wework}
  "fast_gpt": false,                                           # 标识模型接口是否是fastgpt
  "ntchat_smart": false,                                    # 配置ntchat多开，为true时接管当前已登录微信，默认true
  "wework_smart": false,                                 # 配置wework多开，为true时接管当前已登录企业微信，默认true
  "fastgpt_list": {
        "R:108864****63985": "fastgpt-1aps*****pg47-64b16a*******181317",
        "R:107******373863": "fastgpt-1aps8*****gni1kpg47-64b168*****cd181267"
    },							# 每个群聊ID配置对应的key即可实现单群单知识库，未配置的默认
  "wework_http": "http://127.0.0.1:8000",  # weworktop通道http接口地址，默认127.0.0.1:8000
  "wework_callback_port": 8001,  # weworktop回调端口
 }
```
**配置说明：**

**1.个人聊天**

+ 个人聊天中，需要以 "bot"或"@bot" 为开头的内容触发机器人，对应配置项 `single_chat_prefix` (如果不需要以前缀触发可以填写  `"single_chat_prefix": [""]`)
+ 机器人回复的内容会以 "[bot] " 作为前缀， 以区分真人，对应的配置项为 `single_chat_reply_prefix` (如果不需要前缀可以填写 `"single_chat_reply_prefix": ""`)

**2.群组聊天**

+ 群组聊天中，群名称需配置在 `group_name_white_list ` 中才能开启群聊自动回复。如果想对所有群聊生效，可以直接填写 `"group_name_white_list": ["ALL_GROUP"]`
+ 默认只要被人 @ 就会触发机器人自动回复；另外群聊天中只要检测到以 "@bot" 开头的内容，同样会自动回复（方便自己触发），这对应配置项 `group_chat_prefix`
+ 可选配置: `group_name_keyword_white_list`配置项支持模糊匹配群名称，`group_chat_keyword`配置项则支持模糊匹配群消息内容，用法与上述两个配置项相同。（Contributed by [evolay](https://github.com/evolay))
+ `group_chat_in_one_session`：使群聊共享一个会话上下文，配置 `["ALL_GROUP"]` 则作用于所有群聊

**3.语音识别**

+ 添加 `"speech_recognition": true` 将开启语音识别，默认使用openai的whisper模型识别为文字，同时以文字回复，该参数仅支持私聊 (注意由于语音消息无法匹配前缀，一旦开启将对所有语音自动回复，支持语音触发画图)；
+ 添加 `"group_speech_recognition": true` 将开启群组语音识别，默认使用openai的whisper模型识别为文字，同时以文字回复，参数仅支持群聊 (会匹配group_chat_prefix和group_chat_keyword, 支持语音触发画图)；
+ 添加 `"voice_reply_voice": true` 将开启语音回复语音（同时作用于私聊和群聊），但是需要配置对应语音合成平台的key，由于itchat协议的限制，只能发送语音mp3文件，若使用wechaty则回复的是微信语音。

**4.其他配置**

+ `model`: 模型名称，目前支持 `gpt-3.5-turbo`, `text-davinci-003`, `gpt-4`, `gpt-4-32k`  (其中gpt-4 api暂未完全开放，申请通过后可使用)
+ `temperature`,`frequency_penalty`,`presence_penalty`: Chat API接口参数，详情参考[OpenAI官方文档。](https://platform.openai.com/docs/api-reference/chat)
+ `proxy`：由于目前 `openai` 接口国内无法访问，需配置代理客户端的地址，详情参考  [#351](https://github.com/zhayujie/chatgpt-on-wechat/issues/351)
+ 对于图像生成，在满足个人或群组触发条件外，还需要额外的关键词前缀来触发，对应配置 `image_create_prefix `
+ 关于OpenAI对话及图片接口的参数配置（内容自由度、回复字数限制、图片大小等），可以参考 [对话接口](https://beta.openai.com/docs/api-reference/completions) 和 [图像接口](https://beta.openai.com/docs/api-reference/completions)  文档，在[`config.py`](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/config.py)中检查哪些参数在本项目中是可配置的。
+ `conversation_max_tokens`：表示能够记忆的上下文最大字数（一问一答为一组对话，如果累积的对话字数超出限制，就会优先移除最早的一组对话）
+ `rate_limit_chatgpt`，`rate_limit_dalle`：每分钟最高问答速率、画图速率，超速后排队按序处理。
+ `clear_memory_commands`: 对话内指令，主动清空前文记忆，字符串数组可自定义指令别名。
+ `hot_reload`: 程序退出后，暂存微信扫码状态，默认关闭。
+ `character_desc` 配置中保存着你对机器人说的一段话，他会记住这段话并作为他的设定，你可以为他定制任何人格      (关于会话上下文的更多内容参考该 [issue](https://github.com/zhayujie/chatgpt-on-wechat/issues/43))
+ `subscribe_msg`：订阅消息，公众号和企业微信channel中请填写，当被订阅时会自动回复， 可使用特殊占位符。目前支持的占位符有{trigger_prefix}，在程序中它会自动替换成bot的触发词。

**本说明文档可能会未及时更新，当前所有可选的配置项均在该[`config.py`](https://github.com/zhayujie/chatgpt-on-wechat/blob/master/config.py)中列出。**

## 运行

### 1.本地运行（默认Wechat客户端，仅限window平台）

如果是开发机 **本地运行**，直接在项目根目录下执行：

```bash
python3 app.py
```
### 2. PC本地部署wechat（仅限window平台）

1.主项目安装主要依赖后，还需要安装ntchat依赖

```
pip install ntchat
```

2.安装指定PC微信版本：[WeChat3.6.0.18版本](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.6.0.18/WeChatSetup-3.6.0.18.exe)，扫码登陆好，关闭自动更新微信

3.修改主项目配置项：config.json文件内

```json
"channel_type": "ntchat"
```

4.运行 app.py

### 3. PC本地部署wework（仅限window平台）

1.主项目安装主要依赖后，还需要安装ntchat依赖

```
pip install ntwork
```

2.安装指定PC企微专用版本：[WeCom_4.0.8.6027版本](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.6.0.18/WeChatSetup-3.6.0.18.exe)，扫码登陆好，关闭自动更新企业微信

3.修改主项目配置项：config.json文件内

```json
"channel_type": "wework"
```

4.运行 app.py

### 4. PC本地部署高级企微接口（仅限window平台）

1.安装指定PC企微专用版本：[WeCom_4.0.8.6027版本](https://github.com/tom-snow/wechat-windows-versions/releases/download/v3.6.0.18/WeChatSetup-3.6.0.18.exe)，扫码登陆好，关闭自动更新企业微信

2.修改主项目配置项：config.json文件内

```json
"channel_type": "weworktop"
```

3.管理员运行企微接口程序，基础版在项目文件夹”WeChat-AIChatbot-WinOnly\channel\weworktop\“内，运行WeworkApi.exe，不用输入key直接点击启动服务，启动成功企微打开后下一步

4.运行 app.py

## **交流群**

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/bot.jpg)

添加bot，发送  **进群：【一胜Net】AIGC交流** 给bot即可



## 硬核功能展示

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/001.png)

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/002.png)

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/003.png)

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/004.png)

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/005.png)

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/006.png)

![](https://github.com/chazzjimel/WeChat-AIChatbot-WinOnly/blob/main/docs/images/007.png)
