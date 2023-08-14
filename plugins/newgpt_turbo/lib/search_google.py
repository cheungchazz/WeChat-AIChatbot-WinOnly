import concurrent
import urllib
import openai
import requests

from datetime import datetime
from bs4 import BeautifulSoup
from common.log import logger
from concurrent.futures import ThreadPoolExecutor, as_completed

"""谷歌独立搜索函数，通过访问相关URL并提交给GPT整理获得更详细的信息"""

__all__ = ['search_google']
__author__ = 'chazzjimel/跃迁'
__date__ = '2023.6.21'


def get_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        paragraphs_text = [p.get_text() for p in paragraphs]
        return paragraphs_text
    except requests.exceptions.RequestException as e:
        logger.warning("无法访问该URL: %s, error: %s", url, str(e))
        return None



def build_search_url(searchTerms, base_url, count=None, startIndex=None, language=None, cx=None, hq=None,
                     dateRestrict=None,
                     key=None):
    """
    构建谷歌搜索的URL

    :param searchTerms: 搜索关键词
    :param base_url: 基础URL
    :param count: 搜索结果数量
    :param startIndex: 搜索结果的起始位置
    :param language: 搜索结果的语言
    :param cx: 自定义搜索引擎ID
    :param hq: 搜索结果的域名
    :param dateRestrict: 搜索结果的时间限制
    :param key: API密钥
    :return: 构建好的URL
    """
    params = {
        "q": searchTerms,  # 搜索关键词
        "num": count,  # 搜索结果数量
        "start": startIndex,  # 搜索结果的起始位置
        "lr": language,  # 搜索结果的语言
        "cx": cx,  # 自定义搜索引擎ID
        "sort": "date",  # 搜索结果的排序方式
        "filter": 1,  # 是否过滤重复结果
        "hq": hq,  # 搜索结果的域名
        "dateRestrict": dateRestrict,  # 搜索结果的时间限制
        "key": key,  # API密钥
        "alt": "json"  # 返回结果的格式
    }

    params = {k: v for k, v in params.items() if v is not None}  # 去除值为None的参数

    encoded_params = urllib.parse.urlencode(params)  # 对参数进行URL编码

    base_url = base_url  # 基础URL
    search_url = base_url + encoded_params  # 构建完整的URL

    return search_url


def get_summary(item, model, search_terms):
    logger.debug("正在获取链接内容：%s", item["link"])
    link_content = get_url(item["link"])
    if not link_content:
        logger.warning("无法获取链接内容：%s", item["link"])
        return None
    logger.debug("link_content: %s", link_content)
    # 获取链接内容字符数量
    link_content_str = ' '.join(link_content)
    content_length = len(link_content_str)
    logger.debug("content_length: %s", content_length)

    # 如果内容少于200个字符，则pass
    if content_length < 200:
        logger.warning("链接内容低于200个字符：%s", item["link"])
        return None
    # 如果内容大于15000个字符，则截取中间部分
    elif content_length > 8000:
        logger.warning("链接内容高于15000个字符，进行裁断：%s", item["link"])
        start = (content_length - 8000) // 2
        end = start + 8000
        link_content = link_content[start:end]

    logger.debug("正在提取摘要：%s", link_content)
    summary = process_content(str(link_content), model=model, search_terms=search_terms)
    return summary


def search_google(model, base_url, search_terms, count, api_key, cx_id, iterations):
    all_summaries = []

    for i in range(iterations):
        try:
            startIndex = i * count + 1
            search_url = build_search_url(search_terms, base_url=base_url, count=10, cx=cx_id, key=api_key,
                                          startIndex=startIndex)
            logger.debug("正在进行第 %d 次搜索，URL：%s", i + 1, search_url)
            response = requests.get(search_url)
            model = model
            if response.status_code == 200:
                items = response.json().get('items', [])
                logger.debug(f"search_google items:{items}")

                with ThreadPoolExecutor(max_workers=5) as executor:
                    future_to_item = {executor.submit(get_summary, item, model, search_terms): item for item in items}
                    for future in as_completed(future_to_item):
                        try:
                            summary = future.result(timeout=5)  # 设置超时时间
                            if summary is not None:
                                all_summaries.append("【搜索结果内容摘要】：\n" + summary)
                        except concurrent.futures.TimeoutError:
                            logger.error("处理摘要任务超时")
                        except Exception as e:
                            logger.error("在提取摘要过程中出现错误：%s", str(e))
            else:
                logger.error(f"Request failed with status code {response.status_code}")

            # time.sleep(1)  # Delay to prevent rate limiting

        except Exception as e:
            logger.error("在执行搜索过程中出现错误：%s", str(e))

    # 判断 all_summaries 是否为空
    if not all_summaries:
        return ["实时联网暂未获取到有效信息内容，请更换关键词或再次重试······"]

    return all_summaries


def process_content(content, model, search_terms=None):
    current_date = datetime.now().strftime("%Y年%m月%d日")
    summary = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system",
             "content": f"""当前中国北京日期：{current_date}，请判断并提取内容中与"{search_terms}"有关的详细内容，必须保留细节，准确的时间线以及富有逻辑的排版！如果与时间、前因后果、上下文等有关内容不能忽略，不可以胡编乱造！"""},
            {"role": "assistant", "content": content},
        ],
        temperature=0.8
    )
    return summary["choices"][0]["message"]["content"]
