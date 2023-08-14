## 插件描述

本插件将前置文本由GPT判断是否调用函数，集合各种api，实现联网获取信息。

## 使用说明

在 [`AlAPI`](https://alapi.cn/)获取`API key`，获取Bing Search的Key（自行谷歌）

将`config.json.template`复制为`config.json`，修改`API key`和`Bing Search key。

```json
{
  "alapi_key":"", #  使用morning_news_api_key
  "bing_subscription_key": ""， # 使用bing_subscription_key,如果没有则随便输入
  "functions_openai_model":"", #  函数调用模型，可选gpt-3.5-turbo-0613，gpt-4-0613
  "assistant_openai_model":"", #  汇总模型，建议16k
  "temperature":, #  温度 0-1.0
  "max_tokens":, #  返回tokens限制
  "app_key":"", #  nowapi  app_key
  "app_sign":""#   nowapi  app_sign
}

```

## 实现功能

- [x] 新闻早报
- [x] 实时天气
- [x] 每日油价
- [x] 必应搜索（偶尔出问题，待后续优化长文本整理）
- [x] 歌曲信息（渣渣）
- [x] 热榜信息（有点渣）
- [x] 星座运势（部分无数据）
- [x] 全球实时日期时间
- [x] Get-Url（分析汇总网页）
