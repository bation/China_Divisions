import requests
import json
import os
from bs4 import BeautifulSoup

HOME_PATH = os.path.expandvars('$HOME')
DIR_NAME = os.path.join(HOME_PATH, '中华人民共和国县级及以上行政区划代码(code-divisions)')


def get_area_code_dict(soup, year):
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
        for td, i in zip(td_list[0:], range(0, len(td_list[0:]))):
            # if td.string is None:
            #     continue
            # else:
            if code == '':
                for s in td.stripped_strings:
                    # print(str(s))
                    code = str(s)

            else:
                for s in td.stripped_strings:
                    # print(str(s))
                    city = str(s)
        print(city + '-' + code)
        print(year)
        code_dict[code] = city
        code = ''
        city = ''
    # print(code_dict)
    jsObj = json.dumps(code_dict, ensure_ascii=False)

    YEAR_NAME = os.path.join(DIR_NAME, '1980-2018年度数据')

    if not os.path.exists(YEAR_NAME):
        os.makedirs(YEAR_NAME)
    file_path = os.path.join(YEAR_NAME, '%s.json' % year)
    with open(file_path, 'w') as jsonFile:
        jsonFile.write(jsObj)
    return code_dict


def load_data_html():
    code_dict = {}
    with open('source.json') as jsonFile:
        source_json = json.load(jsonFile)
    # print(source_json)
    for i in range(1980, 2019):
    # for i in range(1980, 1981):
        url = source_json[str(i)]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        code_dict.update(get_area_code_dict(soup, i))

    jsObj = json.dumps(code_dict, ensure_ascii=False)
    file_path = os.path.join(DIR_NAME, '1980-2018县级及以上行政区划代码汇总（已去重）.json')
    with open(file_path, 'w') as jsonFile:
        jsonFile.write(jsObj)


if __name__ == '__main__':
    load_data_html()

