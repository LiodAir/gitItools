# encoding:utf-8
import requests
from openpyxl import load_workbook
from selenium import webdriver
import argparse,time
from multiprocessing.dummy import Pool as ThreadPool

def code_Serch(keyword="", **kwargs):
    """
    代码搜索参数
    :param keyword:
    :return:
    """
    q = "q={}".format(keyword)
    type="{}".format(kwargs.get("type")) if kwargs.get("type")!= None else "Code"
    sort = "updated"
    api_url = "https://api.github.com/search/code?q={0}&type={1}&sort={2}&order={3}&access_token={4}&page={5}&per_page=30".format(
        q,
        type,
        sort,
        "sort",
        kwargs.get("api_token"),
        kwargs.get("page")
    )
    print(api_url)
    status = requests.get(api_url).json()
    return status["items"]


def start(limit = 0, keyword="", language=""):
    w = load_workbook("./new.xlsx")
    b = w.worksheets[0]
    content = []
    result = code_Serch(keyword="'{}'+language:{}".format(keyword, language),
               type="Code",
               api_token=api_token,
               page=limit
               )
    print(len(result))
    for r in result:
        cc = {}
        print("*"*90)
        cc.update({"cc-url": r["url"]})
        cc.update({"comment-usrl": "https://github.com/" + r["repository"]["full_name"] + "/blob/master/" + r["path"]})

        print("用户:     {}".format(r["repository"]["owner"]["login"]))
        print("用户主页:  {}".format(r["repository"]["owner"]["url"]))
        cc.update({"username":r["repository"]["owner"]["login"], "user_url": r["repository"]["owner"]["url"]})
        print(cc)
        content.append(cc)
        print("*"*90)


    for t in content:
        b.append([t["username"], t["user_url"], t["comment-usrl"]])

    w.save("./new.xlsx")
    print("文件写入成功")
    print(limit)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="github代码搜索辅助工具")
    parser.add_argument("-p", "--page", help="脚本爬取页数,默认50页")
   # parser.add_argument("-t", "--threading", help="线程数，默认20线程")
    parser.add_argument("-k", "--keyword", help="搜索的关键字")
    parser.add_argument("-l", "--language", help="爬取的语言类型",)
    parser.add_argument("-a", "--apitoken", help="你的github的apikey")
    args = parser.parse_args()
    #global pool
    global api_token
    global keyword
    global language
    #pool = ThreadPool(10) 多线程无法使用，单个api限速
    if args.keyword and args.language and args.apitoken:
        keyword = args.keyword
        language = args.language
        api_token = args.apitoken
        for i in range(50):
            print("开始爬取第%s"%str(i))
            start(i, keyword, language)
            # api 接口延时 github限制速率
            time.sleep(15)

    else:
        parser.print_help()

    
