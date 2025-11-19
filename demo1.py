import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Referer': 'http://osta.mohrss.gov.cn/skillStandard',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
}

params = {
    'pageSize': '10',
    'pageNum': '1',
    'total': '654',
    'nameCode': '起重',
    'status': '1',
}

response = requests.get(
    'http://osta.mohrss.gov.cn/api/public/skillStandardList',
    params=params,
    headers=headers,
    verify=False,
)

print(response.text)