import os
import json
import pymysql


def load_code_json():
    file_dir = os.path.join(os.path.expandvars("$HOME"), '中华人民共和国县级及以上行政区划代码(code-divisions)')
    file_name = os.path.join(file_dir, '1980-2018县级及以上行政区划代码汇总（已去重）.json')

    with open(file_name) as code_file:
        code_json = json.load(code_file)
    return code_json


def save_division(cursor, code, city, district, name, province):
    cursor.execute(
        'INSERT INTO zhangsx.tbl_chmpay_divisions(code, city, district, name, province) VALUES (%s, %s, %s, %s, %s)',
        [code, city, district, name, province])


def main():
    # 连接数据库
    mysqlHost = "localhost"
    mysqlUser = "root"
    mysqlPassword = ""
    mysqlDbName = "zhangsx"
    db = pymysql.connect(mysqlHost, mysqlUser, mysqlPassword, mysqlDbName)
    # 获取游标
    cursor = db.cursor()

    divisions_dict = load_code_json()
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
        if province == city:
            city = value
            value = '-'
            name = province.strip() + city.strip()

        try:
            save_division(cursor, code.strip(), city.strip(), value.strip(), name.strip(), province.strip())
        except Exception as e:
            print("插入出错")
            print(e)
            db.rollback()
    db.commit()
    db.close()


if __name__ == '__main__':
    main()
