import pymysql

# 创建一个字典，保存行政代码信息
divisionDict = {}

# 打开2018.txt 文件，解析每一行数据放入字典
f = open("/Users/zhangshuxin/2018.txt")
line = f.readline()
while line:
    # print(line, end='')
    line = line.replace('"', '')
    line = line.replace(' ', '')
    line = line.replace(',', '')
    # print(line)
    line = line.split(':')
    divisionDict[line[0]] = line[1]
    line = f.readline()
f.close()

# 连接数据库
mysqlHost = "localhost"
mysqlUser = "root"
mysqlPassword = "zhangsx"
mysqlDbName = "idauth"
db = pymysql.connect(mysqlHost, mysqlUser, mysqlPassword, mysqlDbName)
# 获取游标
cursor = db.cursor()
# 遍历divisionDict
def saveDivision(cursor, code, city, district, name, province):
    try:
        cursor.execute(
            'INSERT INTO idauth.gb2260_v2018(code, city, district, name, province) VALUES (%s, %s, %s, %s, %s)',
            [code, city, district, name, province])
    except:
        print("插入出错")
        db.rollback()


for key, value in divisionDict.items():
    code = key
    provinceCode = key[0:2] + '0000'
    cityCode = key[0:4] + '00'

    province = divisionDict.get(provinceCode)
    city = divisionDict.get(cityCode)
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
db.commit()
db.close()
