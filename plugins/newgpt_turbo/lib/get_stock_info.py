import json
import random

from urllib.request import urlopen
from urllib.parse import urlencode
from common.log import logger

__all__ = ['get_stock_info']
__author__ = 'chazzjimel/跃迁'
__date__ = '2023.6.21'


def get_all_stocks(appkey, sign):
    """获取所有股票的列表"""
    url = 'http://api.k780.com'
    params = {
        'app': 'finance.stock_list',
        'appkey': appkey,
        'sign': sign,
        'format': 'json',
    }
    params = urlencode(params)

    f = urlopen('%s?%s' % (url, params))
    nowapi_call = f.read()
    a_result = json.loads(nowapi_call.decode('utf-8'))
    return a_result['result']['lists']


def get_symbol_by_name(stock_name, all_stocks):
    """在所有股票列表中查找符合条件的股票"""
    for stock in all_stocks:
        if stock_name in stock['sname']:
            return stock['symbol']
    return None



def get_stock_info(stock_names, appkey, sign):
    """获取股票信息的实现代码"""
    all_stocks = get_all_stocks(appkey, sign)  # 获取所有股票列表
    stoSym_list = []  # 存储符合条件的股票代码

    for stock_name in stock_names.split():  # 遍历输入的股票名称
        stoSym = get_symbol_by_name(stock_name, all_stocks)  # 获取股票代码
        if stoSym:
            stoSym_list.append(stoSym)  # 如果找到了符合条件的股票代码，就添加到列表中
        else:
            logger.debug(f"无法找到股票名称为 {stock_name} 的股票代码")  # 如果找不到符合条件的股票代码，就输出日志

    if not stoSym_list:
        logger.debug("无法找到提供的股票名称的股票代码")  # 如果找不到任何符合条件的股票代码，就输出日志
        return "无法找到提供的股票名称的股票代码"  # 返回错误消息

    stoSym = ",".join(stoSym_list)  # 将符合条件的股票代码用逗号连接成字符串

    url = 'http://api.k780.com'
    params = {
        'app': 'finance.stock_realtime',
        'stoSym': stoSym,
        'appkey': appkey,
        'sign': sign,
        'format': 'json',
    }
    params = urlencode(params)

    try:
        f = urlopen('%s?%s' % (url, params))
        nowapi_call = f.read()
        a_result = json.loads(nowapi_call.decode('utf-8'))

        if a_result:
            if a_result['success'] == '1':
                logger.debug(a_result['result'])  # 如果成功获取股票信息，就输出日志
                return a_result['result']  # 返回股票信息
            else:
                logger.debug(a_result['msg'])  # 如果获取股票信息失败，就输出日志
                return a_result['msg']  # 返回错误消息
        else:
            raise ValueError
    except Exception:
        error_msgs = [
            "对不起，我们无法获取股票信息",
            "糟糕，获取股票信息现在不可用",
            "抱歉，股票搜索遇到了问题",
            "哎呀，获取股票信息似乎出了些问题"
        ]
        return {"error": random.choice(error_msgs)}  # 随机选择一个错误消息返回


