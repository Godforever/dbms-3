# -*- coding: utf-8 -*-

import sys
import datetime
import pymysql

def connect_mysql():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='au87bt49',
                                 db='social_net',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def login(username, password):
    connection = connect_mysql()
    message = 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT password FROM users WHERE username=%s"
            message = 10
            cursor.execute(sql, (username))
            result = cursor.fetchone()
            if result is None:
                message = 1
            else:
                result_password = result['password']
                if result_password != password:
                    message = 2
                else:
                    message = 3
    except:
        connection.rollback()
    finally:
        connection.close()
        return message

def register(username,nickname, name, sex, birth_date, email, address, password):
    # message = 0 表示注册失败， =1表示用户已存在， =2 表示注册成功
    connection = connect_mysql()
    message = 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT username FROM users WHERE username=%s"
            cursor.execute(sql, (username))
            result = cursor.fetchone()
            if result is not None:
                message = 1
            else:
                sql = "INSERT INTO users (username, nickname, name, sex, birthdate, " \
                      "email, address, password)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (username, nickname, name, sex, birth_date, email, address, password))
                sql = "INSERT INTO friends(username, friend_username) VALUES(%s, %s)"
                cursor.execute(sql, (username, username))
                message = 2
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message


def update_personal_information(username=None,
                                nickname = None,
                                name=None,
                                sex=None,
                                birth_date=None,
                                email=None,
                                address=None,
                                password=None):

    message = 0
    if username is None:
        return message

    if (username is None and name is None and sex is None and birth_date is None and email is None and address is None and password is None):
        message = "All the information can't be null!"
        return 1
    connection = connect_mysql()
    try:
        with connection.cursor() as cursor:
            sql = 'UPDATE users SET '
            if nickname is not None:
                sql = sql + 'nickname=%s '
            if name is not None:
                sql = sql + ', name = "' + name +'" '
            if sex is not None:
                sql = sql + ', sex = "' + sex + '" '
            if birth_date is not None:
                sql = sql + ', birthdate = "' + birth_date + '" '
            if email is not None:
                sql = sql + ', email = "' + email +'" '
            if address is not None:
                sql = sql + ', address = "' + address + '" '
            if password is not None:
                sql = sql + ', password = "' + password +'" '
            sql = sql + 'WHERE username = %s'
            print(sql%(nickname, username))
            cursor.execute(sql, (nickname, username))
            message = 2
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message

def insert_update_education_experience(username = None, level = None, start_date = None, end_date = None,
                                school_name = None, degree = None):
    connection = connect_mysql()
    message = 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT username FROM education_experience WHERE username=%s and level=%s"
            cursor.execute(sql, (username,level))
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO education_experience (`username`, `level`, `start_date`, `end_date`, " \
                      "`school_name`, `degree`)VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (username, level, start_date, end_date,school_name, degree))
                message = 1
            else:
                sql = 'UPDATE education_experience ' \
                      'SET username=%s, level=%s, start_date=%s, end_state=%s, school_name=%s,degree=%s' \
                      'WHERE username = %s'
                cursor.execute(sql, ( level, start_date, end_date,school_name, degree, username))
                message = 1

        connection.commit()
    except:
        message = 2
    finally:
        connection.close()
        return message

def insert_update_work_experience(username=None, employer=None,
                                  start_date=None,end_date=None,
                                  position=None):
    connection = connect_mysql()
    message = 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT username FROM work_experience WHERE username=%s and employer=%s"
            cursor.execute(sql, (username, employer))
            result = cursor.fetchone()
            if result is None:
                sql = "INSERT INTO work_experience(`username`, `employer`, `start_date`, `end_date`, " \
                      "`position`)VALUES(%s,%s,%s,%s,%s)"
                cursor.execute(sql, (username, employer, start_date, end_date, position))
                message = 1
            else:
                sql = 'UPDATE work_experience SET ' \
                      '`employer` = %s, `start_date`=%s, `end_date`=%s, `position`=%s' \
                      'WHERE `username`=%s'
                cursor.execute(sql, (employer, start_date, end_date, position, username))
                message = 2

        connection.commit()
    except:
        connection.rollback()

    finally:
        connection.close()
        return message

def search_user(username):
    connection = connect_mysql()
    result = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return result


def search_friend(username, friend_username):
    # 使用笛卡尔积操作实现好基本信息的查询
    connection = connect_mysql()
    result = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT users.username, users.name, users.sex, users.birthdate, users.email, users.address, friends.group " \
                  "FROM users, friends" \
                  "where users.username = %s and friends.username = %s  and friends.friend_username = %s"
            cursor.execute(sql, (friend_username, username, friend_username))
            result = cursor.fetchall()

        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return result

def add_friend(username=None, friend_username=None, group=None):
    connection = connect_mysql()
    message = 0
    if username is None or friend_username is None:
        message = 1
        return message
    try:
        if search_friend(username, friend_username) is None:
            with connection.cursor() as cursor:
                if group is None or group=='my_friends':
                    sql = "INSERT INTO friends(`username`, `friend_username`) VALUES(%s,%s)"
                    cursor.execute(sql, (username, friend_username))
                    message = 2
                else:

                    sql = "INSERT INTO friends(`username`, `friend_username`, `group`) VALUES(%s, %s, %s)"
                    print(sql%(username, friend_username, group))
                    cursor.execute(sql, (username, friend_username, group))
                    message = 2
            connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message

def delete_friend(username=None, friend_username=None):
    connection = connect_mysql()
    message = 0
    if username is None or friend_username is None:
        message = "Username or friend_username can't be none!"
        return message
    try:
        with connection.cursor() as cursor:
            if search_friend(username, friend_username) is None:
                message = 1
                return message
            else:
                sql = "DELETE * FROM friends WHERE username = %s and friend_username = %s"
                cursor.execute(sql, (username, friend_username))
                message = 2
        connection.commit()
    except:
        connection.rollback()
    finally:
        return message

def add_group(username, group_name):
    connection = connect_mysql()
    message = None
    if username is None or group_name is None:
        message = "Username or group_name can't be none!"
        return message
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO friends (username, group) VALUES(%s,%s)"
            cursor.execute(sql, (username, group_name))
            message = "Add group successfully!"
        connection.commit()
    except:
        connection.rollback()
    finally:
        return message

def update_group(username, pre_group_name, group_name):
    connection = connect_mysql()
    message = 0
    if username is None or pre_group_name is None or group_name is None:
        message = 1
        return message
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE friends SET `group`=%s WHERE `username` = %s and `group` = %s"
            cursor.execute(sql, (group_name, username, pre_group_name))
            message = 2
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message

def delete_group(username, group_name):
    message = update_group(username, group_name, "my_friends")
    return message

def deliver_log(username, text, is_public=False):
        connection = connect_mysql()
        message = 0
        try:
            with connection.cursor() as cursor:
                sql = "SELECT max(log_id) from log"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result['max(log_id)'] is None:
                    log_id = 1
                else:
                    log_id = result['max(log_id)'] + 1
                date = datetime.datetime.now()
                if is_public:
                    public = 1
                else:
                    public = 0
                sql = "INSERT INTO log(log_id, username, last_date, log_content, public)VALUES (%s, %s, %s, %s,%s)"
                cursor.execute(sql,(log_id, username, str(date), text, public))
                sql = "INSERT INTO reply(log_id, reply_date, reply_content, username, to_username)VALUES (%s, %s, %s, %s,%s)"
                cursor.execute(sql, (log_id, str(date), " ", username, username))
                message = 1
            connection.commit()
        except:
            connection.rollback()
        finally:
            connection.close()
            return message

def update_log(username, log_id, text, is_public=False):
    connection = connect_mysql()
    message = None
    try:
        with connection.cursor() as cursor:
            date = datetime.datetime.now()
            if is_public:
                public = 0
            else:
                public = 1
            sql = "UPDATE log SET last_date, log_content, public)VALUES (%s, %s,%s) WHERE username = %s and log_id = %s"
            cursor.execute(sql, (str(date), text, public, username, log_id))
            message = "Update the journal successfully!"
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message

def delete_log(username, log_id):
    connection = connect_mysql()
    message = None
    try:
        with connection.cursor() as cursor:
            sql = "DELETE * FROM reply WHERE log_id = %s"
            cursor.execute(sql, (log_id))
            sql = "DELETE * FROM log WHERE log_id = %s and username = %s"
            cursor.execute(sql, (log_id, username))
            message = "Delete the journal successfully"
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message

def add_reply(username, log_id,  reply_content, to_username):
    connection = connect_mysql()
    message = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT max(reply_id) FROM reply WHERE log_id = %s"
            cursor.execute(sql, (log_id))
            result = cursor.fetchone()
            reply_id = result['max(reply_id)'] + 1
            date = datetime.datetime.now()
            sql = "INSERT INTO reply(log_id, reply_id, reply_date, reply_content, username, to_username)VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(log_id, reply_id, str(date), reply_content,username, to_username))
            message = "Add reply successfully!"
        connection.commit()
    except:
        connection.rollback()

    finally:
        connection.close()
        return message

def share_log(sharer_username, log_id):
    connection = connect_mysql()
    message = None
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO share(sharer_username, log_id, share_time, comment_id) VALUES (%s, %s, %s, %s)"
            date = datetime.datetime.now()
            cursor.execute(sql, (sharer_username, log_id, str(date), 0))
            message = "Share journal successfully!"

        connection.commit()
    except:
        connection.rollback()

    finally:
        connection.close()
        return message

def add_comment(username, log_id, comment):
    connection = connect_mysql()
    message = None
    try:
        with connection.cursor() as cursor:
            sql = "SELECT max(comment_id) FROM share WHERE log_id = %s and sharer_username = %s"
            cursor.execute(sql, (log_id, username))
            result = cursor.fetchone()
            comment_id = result['max(comment_id)'] + 1
            sql = "SELECT share_time FROM share WHERE log_id = %s and sharer_username = %s and comment_id = %s"
            cursor.execute(sql, (log_id, username, 0))
            result = cursor.fetchone()
            comment_time = datetime.datetime.now()
            share_time = result['share_time']
            sql = 'INSERT INTO share(sharer_username, log_id, comment_id, share_time, comment, comment_time) ' \
                  'VALUES(%s, %s, %s, %s, %s, %s'
            cursor.execute(sql, (username, log_id, comment_id, share_time, comment, str(comment_time)))
            message = "Add comment successfully!"

        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message


def load_information(username):
    connection = connect_mysql()
    results, message = [None, None, None], 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username))
            results[0] = cursor.fetchone()
            sql = "SELECT * FROM education_experience WHERE username = %s"
            cursor.execute(sql, (username))
            results[1] = cursor.fetchall()
            sql = "SELECT * FROM work_experience WHERE username = %s"
            cursor.execute(sql, (username))
            results[2] = cursor.fetchall()
            message = 1
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return results, message


def load_logs(username):
    #使用嵌套查询以及内连接加载日志以及相应的评论
    connection = connect_mysql()
    results, message = [], 0
    try:
        with connection.cursor() as cursor:


            sql = "SELECT friend_username FROM friends group by username"
            sql = "SELECT friend_username FROM friends WHERE username = %s"
            cursor.execute(sql, (username))
            user_results = cursor.fetchall()
            users = []
            for result in user_results:
                users.append(result['friend_username'])
            # 加载共享文章、用户自己的以及好友的日志
            sql = "SELECT * FROM log WHERE username in(%s) or public = 1"
            in_p = ', '.join((map(lambda x: '%s', users)))
            cursor.execute(sql % in_p, users)
            logs = cursor.fetchall()
            # 加载自己和好友转发的文章
            sql = "SELECT * FROM log natural join share " \
                  "WHERE `log_id` in(SELECT `log_id` from share WHERE `sharer_username` in (%s))"
            in_p = ', '.join((map(lambda x: '%s', users)))
            cursor.execute(sql % in_p, users)
            logs += cursor.fetchall()

            for log in logs:
                sql = "SELECT * FROM reply WHERE log_id=%s and reply_content !=' ' and reply_content !='添加评论' "
                cursor.execute(sql, (log['log_id']))
                replies = cursor.fetchall()
                log['reply'] = replies
                results.append(log)
            message = 3
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return results, message

def create_view_friends():
    connection = connect_mysql()
    message = 0
    try:
        with connection.cursor() as cursor:
            sql = "CREATE VIEW vf as " \
                  "SELECT * FROM friends"
            cursor.execute(sql)
            message = 1
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return message


def load_friends(username):
    connection = connect_mysql()
    results = None
    message = 0
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM vf WHERE username = %s"
            cursor.execute(sql, (username))
            results = cursor.fetchall()
            message = 1

        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return results, message

def loading_logs(username):
    # 使用嵌套查询以及内连接加载日志以及相应的评论
    connection = connect_mysql()
    results, message = [], 0
    try:
        with connection.cursor() as cursor:

            sql = "SELECT friend_username FROM friends group by username"
            cursor.execute(sql, (username))
            user_results = cursor.fetchall()
            users = []
            for result in user_results:
                users.append(result['friend_username'])
            # 加载共享文章、用户自己的以及好友的日志
            sql = "SELECT * FROM log WHERE username in(%s) or public = 1"
            in_p = ', '.join((map(lambda x: '%s', users)))
            cursor.execute(sql % in_p, users)
            logs = cursor.fetchall()
            # 加载自己和好友转发的文章
            sql = "SELECT * FROM log natural join share " \
                  "WHERE `log_id` in(SELECT `log_id` from share WHERE `sharer_username` in (%s))"
            in_p = ', '.join((map(lambda x: '%s', users)))
            cursor.execute(sql % in_p, users)
            logs += cursor.fetchall()

            for log in logs:
                sql = "SELECT * FROM reply WHERE log_id=%s and reply_content !=' ' and reply_content !='添加评论' "
                cursor.execute(sql, (log['log_id']))
                replies = cursor.fetchall()
                log['reply'] = replies
                results.append(log)
            message = 3
        connection.commit()
    except:
        connection.rollback()
    finally:
        connection.close()
        return results, message


if __name__ == "__main__":
    print(create_view_friends())



