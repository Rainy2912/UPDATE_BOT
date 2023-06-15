from ntpath import join
import sqlite3

def join_sql():
    try:
        sql = sqlite3.connect('user.db')
        woogi = sql.cursor()
        return sql, woogi
    except:
        return False, False

def check_data_user(id):
    sql, woogi = join_sql()
    if sql:
        woogi.execute(f"SELECT * FROM user_info WHERE user_id = {id}")
        sql.commit()
        result = woogi.fetchone()
        sql.close()
        if result is None:
            return False
        else:
            return result
    else:
        return False

def my_point(id):
    sql, woogi = join_sql()
    if sql:
        woogi.execute(f"SELECT * FROM user_info WHERE user_id = {id}")
        sql.commit()
        result = woogi.fetchone()
        sql.close()
        if result is None:
            return False
        else:
            return result[2]
    else:
        return False

def plus_my_point(id, plus):
    sql, woogi = join_sql()
    if sql:
        point = my_point(id)
        if point:
            point = int(point)
            woogi.execute(f"UPDATE user_info SET point = {int(point + plus)} WHERE user_id = {id}")
            sql.commit()
            sql.close()
            return int(point + plus)
        else:
            return False
    else:
        return False

def update_my_point(id, min):
    sql, woogi = join_sql()
    if sql:
        point = my_point(id)
        if point:
            point = int(point)
            woogi.execute(f"UPDATE user_info SET point = {int(point - min)} WHERE user_id = {id}")
            sql.commit()
            sql.close()
            return int(point - min)
        else:
            return False
    else:
        return False