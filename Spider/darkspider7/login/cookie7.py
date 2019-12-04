import time
import pymysql

# 连接mysql建库
def sql_save():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root")  # 连接mysql数据库
    cursor = conn.cursor()  # 创建游标对象
    # 创建数据库
    DB_NAME = 'darkspider7'
    cursor.execute('DROP DATABASE IF EXISTS %s' % DB_NAME)  # if 有 则 drop 删除
    time.sleep(1)
    cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % DB_NAME)  # if not 没有则create创建
    conn.select_db(DB_NAME)
    cursor.close()
    conn.close()


# 将cookie保存到mysql
def sql1_save(jsonCookies):
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", database='darkspider7')  # 连接mysql数据库
    cursor = conn.cursor()  # 创建游标对象
    # 创建表
    TABLE_NAME = 'data'
    cursor.execute('CREATE TABLE %s(id int auto_increment primary key ,cookies varchar(2000) null)' % TABLE_NAME)
    # cursor.execute('insert into data(cookies) values (%s)')
    sql = "insert into data(cookies) values (%s);"
    print(jsonCookies)
    cookies = jsonCookies
    cursor.execute(sql, [cookies])
    conn.commit()
    cursor.close()
    conn.close()

