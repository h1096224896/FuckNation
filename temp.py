import re



# 读取txt网页源码
with open("html.txt", "r", encoding="utf-8") as f:
    html = f.read()
    print(html)
    # 利用正则匹配域名
    matches = re.findall(r'(http|https)://([a-zA-Z0-9]+\.[a-zA-Z]{2,3})', html)
    url = []
    for i in matches:
        url.append(i[0] + "://" + i[1])
    # 去重
    url = list(set(url))
    print(url)
    # 写入txt
    with open("url.txt", "w", encoding="utf-8") as f:
        for i in url:
            f.write(i + "\n")