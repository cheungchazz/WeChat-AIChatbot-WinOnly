import json
import time
import urllib.parse
import urllib.request
import urllib.request
import requests
import random

from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode


__author__ = 'chazzjimel/跃迁'
__date__ = '2023.6.21'


# 使用必应搜索API进行搜索并返回相关的网络搜索结果和新闻
def search_bing(query, subscription_key, count):
    """
    使用必应Web搜索API进行搜索并返回相关的网络搜索结果和新闻
    文档：https://docs.microsoft.com/en-us/bing/search-apis/bing-web-search/overview
    """
    # 构造请求
    endpoint = "https://api.bing.microsoft.com/v7.0/search"
    mkt = 'zh-CN'
    count = count
    params = {'q': query, 'mkt': mkt, 'count': count}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    # 调用API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        # 解析响应
        data = response.json()

        # 选择我们需要的数据
        results = {
            'webPages': data.get('webPages', {}).get('value', []),
            'news': data.get('news', {}).get('value', []),
        }

        # 返回解析后的结果
        return results

    except Exception as ex:
        raise ex


def get_morning_news(api_key):
    """获取每日早报、新闻的实现代码"""
    url = "https://v2.alapi.cn/api/zaobao"
    payload = f"token={api_key}&format=json"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        morning_news_info = response.json()
        if morning_news_info['code'] == 200:  # 验证请求是否成功
            return json.dumps(morning_news_info, ensure_ascii=False)
        else:
            raise ValueError
    except Exception:
        error_msgs = [
            "对不起，我们目前无法获取早报新闻信息",
            "糟糕，早报新闻信息现在不可用",
            "抱歉，获取早报新闻信息遇到了问题",
            "哎呀，早报新闻信息似乎不在服务范围内",
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回


def get_hotlist(api_key, type):
    """获取热榜信息的实现代码，但不返回链接信息"""
    type_mapping = {
        "知乎": "zhihu",
        "微博": "weibo",
        "微信": "weixin",
        "百度": "baidu",
        "头条": "toutiao",
        "163": "163",
        "36氪": "36k",
        "历史上的今天": "hitory",
        "少数派": "sspai",
        "CSDN": "csdn",
        "掘金": "juejin",
        "哔哩哔哩": "bilibili",
        "抖音": "douyin",
        "吾爱破解": "52pojie",
        "V2EX": "v2ex",
        "Hostloc": "hostloc",
    }

    # 如果用户直接提供的是英文名，则直接使用
    try:
        if type.lower() in type_mapping.values():
            api_type = type.lower()
        else:
            api_type = type_mapping.get(type, None)
            if api_type is None:
                raise ValueError(f"未知的类型: {type}")

        url = "https://v2.alapi.cn/api/tophub/get"
        payload = {"token": api_key, "type": api_type}
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        response = requests.request("POST", url, data=payload, headers=headers)
        hotlist_info = response.json()
        if hotlist_info['code'] == 200:  # 验证请求是否成功
            # 遍历每个条目，删除它们的 "link" 属性
            for item in hotlist_info['data']['list']:
                item.pop('link', None)
            return hotlist_info['data']  # 返回 'data' 部分
        else:
            raise ValueError
    except Exception:
        error_msgs = [
            "对不起，我们目前无法获取实时热榜信息",
            "糟糕，实时热榜信息现在不可用",
            "抱歉，获取实时热榜信息遇到了问题",
            "哎呀，实时热榜信息似乎不在服务范围内",
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回


def get_current_weather(api_key, city):
    """获取天气的实现代码"""
    url = "https://v2.alapi.cn/api/tianqi"
    payload = {"token": api_key, "city": city}
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        weather_info = response.json()
        if weather_info['code'] == 200:  # 验证请求是否成功
            return weather_info['data']  # 直接返回 'data' 部分
        else:
            raise ValueError
    except Exception:
        error_msgs = [
            "对不起，我们目前无法获取这个城市的天气信息",
            "糟糕，该城市的天气信息现在不可用",
            "抱歉，获取该城市的天气信息遇到了问题",
            "哎呀，该城市的天气信息似乎不在服务范围内",
        ]
        return {"error": random.choice(error_msgs)}  # 随机选择一个错误消息返回


def get_oil_price(api_key):
    """实现全国油价查询的代码"""
    url = "https://v2.alapi.cn/api/oil"
    payload = {"token": api_key}
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        oil_price_info = response.json()
        if oil_price_info['code'] == 200:  # 验证请求是否成功
            return json.dumps(oil_price_info, ensure_ascii=False)
        else:
            raise ValueError
    except Exception:
        error_msgs = [
            "对不起，我们目前无法获取油价信息",
            "糟糕，油价信息现在不可用",
            "抱歉，获取油价信息遇到了问题",
            "哎呀，油价信息似乎不在服务范围内",
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回


def get_Constellation_analysis(api_key, star):
    """实现星座运势查询的代码"""
    star_mapping = {
        "白羊座": "aries",
        "金牛座": "taurus",
        "双子座": "gemini",
        "巨蟹座": "cancer",
        "狮子座": "leo",
        "处女座": "virgo",
        "天秤座": "libra",
        "天蝎座": "scorpio",
        "射手座": "sagittarius",
        "摩羯座": "capricorn",
        "水瓶座": "aquarius",
        "双鱼座": "pisces"
    }

    # 如果用户直接提供的是英文名，则直接使用
    try:
        if star.lower() in star_mapping.values():
            star_english = star.lower()
        else:
            star_english = star_mapping.get(star, None)
            if star_english is None:
                raise ValueError(f"未知的星座: {star}")

        url = "https://v2.alapi.cn/api/star"
        payload = {"token": api_key, "star": star_english}
        headers = {'Content-Type': "application/x-www-form-urlencoded"}

        response = requests.request("POST", url, data=payload, headers=headers)
        constellation_info = response.json()
        if constellation_info['code'] == 200:  # 验证请求是否成功
            return json.dumps(constellation_info, ensure_ascii=False)
        else:
            raise ValueError
    except Exception:
        error_msgs = [
            "对不起，我们目前无法获取这个星座的运势信息",
            "糟糕，该星座的运势信息现在不可用",
            "抱歉，获取该星座的运势信息遇到了问题",
            "哎呀，该星座的运势信息似乎不在服务范围内",
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回



def get_video_url(api_key, target_url):
    """
    通过视频链接获取视频地址
    :param api_key: str, API key
    :param target_url: str, 目标视频链接
    :return: str, 视频地址
    """
    api_url = "https://v2.alapi.cn/api/video/url"
    payload = f"token={api_key}&url={target_url}"
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    # 重试 10 次
    for _ in range(10):
        try:
            response = requests.request("POST", api_url, data=payload, headers=headers)
            response.raise_for_status()  # 如果状态码是 4xx 或 5xx，抛出 HTTPError 异常
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("Something went wrong", err)

        if response.status_code == 200:
            response_json = response.json()
            if 'data' in response_json and response_json['data'] is not None and 'video_url' in response_json['data']:
                return response_json['data']['video_url']

        # 如果响应码不是 200，等待 2 秒然后重试
        time.sleep(2)

    return None


def music_search(api_key, keyword):
    # 第一步：搜索音乐
    search_url = "https://v2.alapi.cn/api/music/search"
    search_payload = {"token": api_key, "keyword": keyword}
    search_headers = {'Content-Type': "application/x-www-form-urlencoded"}

    try:
        search_response = requests.request("POST", search_url, data=search_payload, headers=search_headers)
        search_info = search_response.json()

        if search_info['code'] != 200:  # 如果请求不成功，抛出异常
            raise ValueError

        # 第二步：对每首歌曲获取其URL
        songs_info = search_info['data']['songs']
        result = []
        for song in songs_info:
            song_id = song['id']

            url_payload = {"id": str(song_id), "format": "json", "token": api_key}
            url_response = requests.request("GET", "https://v2.alapi.cn/api/music/url", params=url_payload)

            url_info = url_response.json()
            if url_info['code'] == 200:
                song['url'] = url_info['data']['url']  # 将URL添加到歌曲信息中
            else:
                song['url'] = 'URL获取失败'

            # 获取歌曲名称
            song_name = song['name']
            # 获取歌手
            artists = ", ".join([artist['name'] for artist in song['artists']])
            # 获取时长，单位为毫秒，转换为秒需要除以1000
            duration = song['duration'] / 1000
            # 获取url
            url = song['url']

            # 保存结果
            result.append({
                "song_name": song_name,
                "artists": artists,
                "duration": duration,
                "url": url,
            })

        return result

    except Exception:
        error_msgs = [
            "对不起，我们目前无法搜索到这首音乐",
            "糟糕，该音乐搜索结果现在不可用",
            "抱歉，搜索该音乐遇到了问题",
            "哎呀，该音乐似乎不在服务范围内",
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回


def get_short_link(api_key, url):
    api_url = "https://v2.alapi.cn/api/url"
    payload = {"token": api_key, "url": url}
    headers = {'Content-Type': "application/x-www-form-urlencoded"}

    try:
        response = requests.request("POST", api_url, data=payload, headers=headers)
        short_link_info = response.json()
        if short_link_info['code'] == 200:  # 验证请求是否成功
            return json.dumps(short_link_info, ensure_ascii=False)
        else:
            raise ValueError
    except Exception:
        error_msgs = [
            "对不起，我们目前无法获取这个链接的短链接",
            "糟糕，生成短链接现在不可用",
            "抱歉，生成短链接遇到了问题",
            "哎呀，该链接似乎无法生成短链接",
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回


def get_datetime(appkey, sign, city_en):
    """实现获取全球指定城市的时间代码"""
    url = 'http://api.k780.com'
    params = {
        'app': 'time.world',
        'city_en': city_en,
        'appkey': appkey,
        'sign': sign,
        'format': 'json',
    }

    params = urllib.parse.urlencode(params)
    url_with_params = '%s?%s' % (url, params)

    try:
        f = urllib.request.urlopen(url_with_params)
        nowapi_call = f.read()
        a_result = json.loads(nowapi_call)

        if a_result:
            if a_result['success'] != '0':
                return a_result['result']
            else:
                return a_result['msgid'] + ' ' + a_result['msg']
        else:
            return 'Request nowapi fail.'
    except Exception:
        error_msgs = [
            "对不起，我们目前无法获取该城市的时间信息",
            "糟糕，获取时间信息现在不可用",
            "抱歉，获取时间信息遇到了问题",
            "哎呀，该城市的时间信息似乎无法获取",
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回


# 获取指定URL的内容，并返回一个字符串
def get_url(url):
    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 "
                      "Safari/537.36"
    }

    try:
        # 发送GET请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 抛出HTTP错误状态

        # 解析HTML文档
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')

        # 提取出每个<p>标签的文本内容，得到一个字符串列表
        paragraphs_text = [p.get_text() for p in paragraphs]

        # Join the paragraphs and check the length
        full_text = ''.join(paragraphs_text)

        if len(full_text) > 8000:
            # 如果文本太长，将其截断为8000个字符
            full_text = full_text[:8000]

        # 在full_text前面插入一个字符串"成功访问URL，URL内容："
        full_text = "成功访问URL，URL内容：" + full_text

        return full_text

    except Exception:
        # 如果发生异常，返回一个随机的错误消息
        error_msgs = [
            "对不起，我们无法访问你提供的URL",
            "糟糕，获取网页信息现在不可用",
            "抱歉，访问网页遇到了问题",
            "哎呀，你提供的URL似乎无法获取"
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回


# 实现全球大部分天气和各种指数的函数
def get_weather(cityNm, appkey, sign):
    # API请求地址
    url = 'http://api.k780.com'
    # 请求参数
    params = {
        'app': 'weather.realtime',  # 请求的API名称
        'cityNm': cityNm,  # 城市名称
        'ag': 'today,futureDay,lifeIndex,futureHour',  # 请求的数据类型
        'appkey': appkey,  # API密钥
        'sign': sign,  # API密钥对应的签名
        'format': 'json',  # 返回数据的格式
    }
    # 将请求参数编码为URL格式
    params = urlencode(params)

    try:
        # 发送请求并获取响应
        f = urlopen('%s?%s' % (url, params))
        nowapi_call = f.read()
        # 将响应数据解码为JSON格式
        a_result = json.loads(nowapi_call.decode('utf-8'))
        if a_result:
            if a_result['success'] != '0':
                # 如果请求成功，返回响应结果
                return a_result['result']
            else:
                # 如果请求失败，返回错误消息
                return a_result['msgid'] + ' ' + a_result['msg']
        else:
            # 如果请求失败，返回错误消息
            return 'Request nowapi fail.'
    except Exception:
        # 如果发生异常，返回一个随机的错误消息
        error_msgs = [
            "对不起，我们无法获取 {} 的天气信息".format(cityNm),
            "获取 {} 的天气信息现在不可用".format(cityNm),
            "获取 {} 的天气信息遇到了问题".format(cityNm),
            "无法获取 {} 的天气信息".format(cityNm)
        ]
        return random.choice(error_msgs)  # 随机选择一个错误消息返回



def search_bing_news(count, subscription_key, query):
    # 设置API的请求地址
    endpoint = "https://api.bing.microsoft.com/v7.0/news/search"

    # 设置其他参数
    mkt = 'zh-CN'

    # 构造请求
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'mkt': mkt, 'q': query, 'count': count}

    try:
        # 发送请求
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # 如果发生网络错误，此句会抛出异常

        # 获取并返回响应数据
        data = response.json()
        return data
    except Exception:
        # 如果发生异常，返回一个随机的错误消息
        error_msgs = [
            "对不起，我们无法获取新闻",
            "糟糕，获取新闻现在不可用",
            "抱歉，新闻搜索遇到了问题",
            "哎呀，获取新闻似乎出了些问题"
        ]
        return {"error": random.choice(error_msgs)}  # 随机选择一个错误消息返回


