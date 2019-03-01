import os
from bs4 import BeautifulSoup

d1 = {'北京': 110, '上海': 120}
d2 = {'上海': 120, '天津': 130}
d3 = {}
d3.update(d1)
d3.update(d2)
HOME_PATH = os.path.expandvars('$HOME')
dirname = os.path.join(HOME_PATH, '中华人民共和国县级及以上行政区划代码')
pathname = os.path.join(dirname, '%s.json' % 2018)
# print(pathname)
with open(os.path.join(HOME_PATH, '111.html')) as f:
    soup = BeautifulSoup(f.read(), 'html5lib')
    print(soup)
    tds = soup.find_all('td')
    for td in tds:
        print(td.string)
        print('stripped_strings-' + str(len(td.stripped_strings)))
        for s in td.stripped_strings:
            print(str(s))
        # print(td.string)
