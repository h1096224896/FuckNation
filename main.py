# 导入所需的库
import requests
import re
import random
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"
}


# 定义一个函数，从文件中读取关键词列表，并返回关键词列表
def get_keywords(filename):
    with open(filename, "r", encoding="utf-8") as f:  # 以只读模式打开文件
        # 读取文件中的每一行，并去掉行末的换行符，然后添加到列表中
        keywords = [line.strip() for line in f.readlines()]
    return keywords  # 返回关键词列表


# 定义一个函数，从文件中读取代理 IP 列表，并返回代理 IP 列表
def get_proxies(filename):
    with open(filename, "r", encoding="utf-8") as f:  # 以只读模式打开文件
        # 读取文件中的每一行，并去掉行末的换行符，然后添加到列表中
        proxies = [line.strip() for line in f.readlines()]
    return proxies  # 返回代理 IP 列表


# 定义一个函数，检测 Google 搜索引擎是否可用，并返回搜索结果页面的源码
def check_google(keyword):
    url = "https://www.google.com/search?q=" + keyword  # 构造搜索链接
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"}  # 设置请求头，模拟浏览器访问
    try:  # 尝试发送请求
        response = requests.get(url, headers=headers,
                                timeout=10)  # 发送请求，并设置超时时间为 10 秒
        # 打印国家代码和响应状态码
        print(keyword, response.status_code)
        if response.status_code == 200:  # 如果响应状态码为 200，表示成功访问
            return response.text  # 返回页面源码
        else:  # 如果响应状态码不为 200，表示访问失败或被拦截
            return None  # 返回空值
    except Exception as e:  # 如果发生异常，表示请求出错或超时
        print(e)  # 打印异常信息
        return None  # 返回空值


# 定义一个函数，从页面源码中提取域名，并过滤重复的网站，只要一级域名，并返回域名列表和所属国家代码（根据域名后缀判断）
def extract_domains(html):
    domains = []  # 定义一个空列表，用于存放域名
    # 定义一个正则表达式，用于匹配域名
    # pattern = re.compile(r'(http|https)://([a-zA-Z0-9]+\.[a-zA-Z]{2,3})')
    pattern = re.compile(r'http[s]?://[^(/<"\\ ]*')
    matches = pattern.findall(html)  # 从页面源码中匹配域名
    # 去掉matches中的重复元素
    matches = list(set(matches))
    url = matches
    return url  # 返回域名列表和所属国家代码


# 定义一个函数，将域名和国家代码的元组列表写入 txt 文档中，每个域名占一行，并记录关键词和时间戳
def write_domains(keyword, domains_url):
    with open("domains.txt", "a", encoding="utf-8") as f:  # 以追加模式打开文件，如果文件不存在则创建
        f.write(f"Keyword: {keyword}\n")  # 写入关键词
        # 写入时间戳
        f.write(
            f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
        for domain, country in domains_url:  # 遍历域名和国家代码的元组列表
            f.write(f"{domain} {country}\n")  # 写入域名和国家代码，用空格分隔
        f.write("\n")  # 写入空行


# 定义一个主函数，实现采集国外网站的功能
def main():
    # keywords = get_keywords("keywords.txt")  # 从文件中读取关键词列表
    # keywords = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo, Democratic Republic of the', 'Congo, Republic of the', 'Costa Rica', 'Cote d\'Ivoire', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kosovo', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar',
    #             'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar (Burma)', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City (Holy See)', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe']

    keywords = open("random_word.txt", "r", encoding="utf-8").readlines()

    # proxies = get_proxies("proxies.txt")  # 从文件中读取代理 IP 列表
    for keyword in keywords:
        # 把keyword写入txt，以便后续插重使用
        with open("./word/记录.txt", 'a', encoding="utf-8") as f:
            f.write(keyword)
        # 如果关键词已经在记录.txt中，跳过
        with open("./word/记录.txt", 'r', encoding="utf-8") as f:
            lines = f.readlines()
            if keyword in lines:
                continue
        html = check_google(keyword)  # 检测 Google 搜索引擎是否可用，并返回搜索结果页面的源码
        if html:  # 如果页面源码不为空，表示访问成功
            # 保存页面源码
            with open("html.txt", "w", encoding="utf-8") as f:
                f.write(html)
            # 从页面源码中提取域名，并过滤重复的网站，只要一级域名，并返回域名列表和所属国家代码
            domains_url = extract_domains(html)

            for url in domains_url:
                try:
                    res = requests.get(url, headers=headers, timeout=10)
                    if res.status_code == 200:
                        print(url, res.status_code)
                        with open("./word/{}.txt".format(keyword), "a", encoding="utf-8") as f:
                            f.write(url + "\t访问成功!" + "\n")
                    # else:
                    #     with open("{}.txt".format(keyword), "a", encoding="utf-8") as f:
                    #         f.write(url + "\t访问失败!" + "\n")
                        continue
                except Exception as e:
                    print(e)
                    print("@@@@@@@@@@注意看这里！！！@@@@@@@")
                    with open("./word/{}.txt".format(keyword), "a", encoding="utf-8") as f:
                        f.write(url + "\t访问失败!" + "\n")
                    continue
            time.sleep(1)
        else:  # 如果页面源码为空，表示访问失败或被拦截
            continue  # 跳过当前关键词，继续下一个关键词


if __name__ == "__main__":  # 如果是主程序
    main()  # 调用主函数
