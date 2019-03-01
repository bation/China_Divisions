import requests
from bs4 import BeautifulSoup

# 获取指定文章的uri列表
def get_article_uri():
    article_list = []
    url = 'http://www.mca.gov.cn/article/sj/xzqh//1980/?'
    # 有三页文章，分三次解析
    for i in range(0, 3):
        if i == 0:
            response = requests.get(url)
        else:
            response = requests.get(url + str(i + 1))
        soup = BeautifulSoup(response.content, "html5lib")
        title_list_url = soup.find_all('a', class_='artitlelist')
        # 获得所有文章的URI
        p = '中华人民共和国行政区划代码（截止'
        for s in title_list_url:
            if p in s['title']:
                article_list.append(s['href'])
    # print(article_list)
    return article_list


# 判断是否是行政代码的html
def is_data_html(soup):
    l = soup.find_all('a')
    print(l)
    if len(l) == 0:
        return True
    else:
        return False


# 获取每一年的行政代码的dict
def get_area_code_dict(soup):
    code_dict = {}
    # print(soup)
    # 获取soup下的所有tr标签
    tr_list = soup.find_all('tr')
    code = ''
    city = ''
    # print(tr_list)
    for tr in tr_list[2:]:
        # 获取tr下的所有td标签
        td_list = tr.find_all('td')
        for td, i in td_list[1:], range(0, len(td_list) - 1):
            if td.string == '':
                continue
            else:
                if i == 1:
                    code = td.string
                else:
                    city = td.string
        code_dict[code] = city
    # print(code_dict)
    return code_dict


def save_area_code():
    MCA_domain = 'http://www.mca.gov.cn'
    area_code_dict = {}
    article_list = get_article_uri()

    i = 0

    for uri in article_list:
        i+=1
        url = MCA_domain + uri
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        # print(soup)
        # # 存文件
        # my_file = open('/Users/zhangshuxin/MCA/'+str(i)+'.html', 'w')
        # my_file.write(response.text)
        # my_file.close()
        area_code_dict.update(get_area_code_dict(soup))
        # print(response.text)
        # if is_data_html(soup):
        #     area_code_dict.update(get_area_code_dict(soup))
        # else:
        #     i += 1
        #     a_list = soup.find_all('A')
        #     for a in a_list:
        #         if '中华人民共和国县以上行政区划代码' in a.string:
        #             data_url = a['data_ue_src']
        #             soup = BeautifulSoup(requests.get(data_url).content, 'html5lib')
        #             area_code_dict.update(get_area_code_dict(soup))
    # print(area_code_dict)
    print(i)
    print(len(article_list))


save_area_code()
