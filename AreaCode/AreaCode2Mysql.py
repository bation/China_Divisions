import os
import json


def load_code_json():
    file_dir = os.path.join(os.path.expandvars("$HOME"), '中华人民共和国县级及以上行政区划代码')
    file_name = os.path.join(file_dir, '1980-2018县级及以上行政区划代码汇总（已去重）.json')

    with open(file_name) as code_file:
        code_json = json.load(code_file)
    return code_json


def split_json(divisions_dict):
    for key, value in divisions_dict.items():
        code = key
        provinceCode = key[0:2] + '0000'
        cityCode = key[0:4] + '00'

        province = divisions_dict.get(provinceCode)
        city = divisions_dict.get(cityCode)
        if city is None:
            city = province

        if code.endswith('0000'):
            name = province.strip()
            city = '-'
            value = '-'
        elif code.endswith('00') and not code.endswith('0000'):
            name = province.strip() + city.strip()
            value = '-'
        else:
            name = province.strip() + city.strip() + value.strip()
        print('name = %s' % name)

        saveDivision(cursor, code.strip(), city.strip(), value.strip(), name.strip(), province.strip())
