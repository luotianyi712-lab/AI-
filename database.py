import sqlite3
import time


DATABASE_NAME = "luotianyi.db"



# =========================
# 数据库连接
# =========================

def get_connection():

    return sqlite3.connect(
        DATABASE_NAME
    )




# =========================
# 初始化数据库
# =========================

def init_database():

    conn = get_connection()

    cursor = conn.cursor()



    # 用户表

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT,

        created_time INTEGER

    )
    """)




    # 聊天记录表

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        role TEXT,

        content TEXT,

        time INTEGER

    )
    """)




    # 情绪表

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emotion (

        user_id INTEGER PRIMARY KEY,

        state TEXT,

        affection INTEGER

    )
    """)




    # 长期记忆表

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        memory_type TEXT,

        content TEXT,

        importance INTEGER,

        time INTEGER

    )
    """)





    # 用户资料表

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER UNIQUE,

        birthday TEXT,

        favorite TEXT,

        hobby TEXT,

        description TEXT

    )
    """)




    conn.commit()

    conn.close()






# =========================
# 创建用户
# =========================

def create_user(username):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        INSERT INTO users

        (
            username,
            created_time
        )

        VALUES (?,?)

        """,
        (
            username,
            int(time.time())
        )
    )


    user_id = cursor.lastrowid





    # 初始化情绪

    cursor.execute(
        """
        INSERT INTO emotion

        (
            user_id,
            state,
            affection
        )

        VALUES (?,?,?)

        """,
        (
            user_id,
            "平静",
            0
        )
    )





    # 初始化用户资料

    cursor.execute(
        """
        INSERT INTO profiles

        (
            user_id,
            birthday,
            favorite,
            hobby,
            description
        )

        VALUES (?,?,?,?,?)

        """,
        (
            user_id,
            "",
            "",
            "",
            ""
        )
    )





    conn.commit()

    conn.close()



    return user_id







# =========================
# 获取用户信息
# =========================

def get_user(user_id):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT username

        FROM users

        WHERE id=?

        """,
        (
            user_id,
        )
    )



    result = cursor.fetchone()


    conn.close()



    if result:

        return {

            "username": result[0]

        }



    return {

        "username": "游客"

    }






# =========================
# 修改用户名
# =========================

def update_username(
    user_id,
    username
):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        UPDATE users

        SET username=?

        WHERE id=?

        """,
        (
            username,
            user_id
        )
    )


    conn.commit()

    conn.close()








# =========================
# 获取用户资料
# =========================

def get_profile(user_id):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT

            birthday,

            favorite,

            hobby,

            description


        FROM profiles


        WHERE user_id=?

        """,
        (
            user_id,
        )
    )



    result = cursor.fetchone()



    conn.close()



    if result:

        return {

            "birthday": result[0],

            "favorite": result[1],

            "hobby": result[2],

            "description": result[3]

        }



    return {

        "birthday": "",

        "favorite": "",

        "hobby": "",

        "description": ""

    }






# =========================
# 更新用户资料
# =========================

def update_profile(
    user_id,
    birthday=None,
    favorite=None,
    hobby=None,
    description=None
):

    conn = get_connection()

    cursor = conn.cursor()



    old = get_profile(
        user_id
    )



    if birthday is None:

        birthday = old["birthday"]


    if favorite is None:

        favorite = old["favorite"]


    if hobby is None:

        hobby = old["hobby"]


    if description is None:

        description = old["description"]





    cursor.execute(
        """
        UPDATE profiles

        SET

            birthday=?,

            favorite=?,

            hobby=?,

            description=?


        WHERE user_id=?

        """,
        (
            birthday,

            favorite,

            hobby,

            description,

            user_id
        )
    )



    conn.commit()

    conn.close()








# =========================
# 保存聊天
# =========================

def save_message(
    user_id,
    role,
    content
):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        INSERT INTO chat_history

        (
            user_id,
            role,
            content,
            time
        )

        VALUES (?,?,?,?)

        """,
        (
            user_id,
            role,
            content,
            int(time.time())
        )
    )



    conn.commit()

    conn.close()







# =========================
# 获取聊天记录
# =========================

def get_history(
    user_id,
    limit=20
):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT

            role,

            content


        FROM chat_history


        WHERE user_id=?


        ORDER BY id DESC


        LIMIT ?

        """,
        (
            user_id,
            limit
        )
    )



    data = cursor.fetchall()



    conn.close()



    data.reverse()



    return [

        {

            "role": item[0],

            "content": item[1]

        }

        for item in data

    ]






# =========================
# 获取情绪
# =========================

def get_emotion(user_id):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT

            state,

            affection


        FROM emotion


        WHERE user_id=?

        """,
        (
            user_id,
        )
    )


    result = cursor.fetchone()



    conn.close()



    if result:

        return {

            "state": result[0],

            "affection": result[1]

        }



    return {

        "state": "平静",

        "affection": 0

    }






# =========================
# 更新情绪
# =========================

def update_emotion(
    user_id,
    state,
    affection
):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        UPDATE emotion

        SET

            state=?,

            affection=?


        WHERE user_id=?


        """,
        (
            state,

            affection,

            user_id

        )
    )


    conn.commit()

    conn.close()






# =========================
# 保存长期记忆
# =========================

def save_memory(
    user_id,
    memory_type,
    content,
    importance=1
):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        INSERT INTO memory

        (
            user_id,

            memory_type,

            content,

            importance,

            time
        )


        VALUES (?,?,?,?,?)

        """,
        (
            user_id,

            memory_type,

            content,

            importance,

            int(time.time())

        )
    )



    conn.commit()

    conn.close()






# =========================
# 获取长期记忆
# =========================

def get_memory(
    user_id,
    limit=10
):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT

            memory_type,

            content


        FROM memory


        WHERE user_id=?


        ORDER BY

            importance DESC,

            id DESC


        LIMIT ?

        """,
        (
            user_id,

            limit

        )
    )


    data = cursor.fetchall()



    conn.close()



    return [

        {

            "type": item[0],

            "content": item[1]

        }

        for item in data

    ]






# =========================
# 搜索已有记忆
# =========================

def search_memory(user_id):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        SELECT

            id,

            memory_type,

            content,

            importance


        FROM memory


        WHERE user_id=?


        ORDER BY importance DESC

        """,
        (
            user_id,
        )
    )



    data = cursor.fetchall()



    conn.close()



    return [

        {

            "id": item[0],

            "type": item[1],

            "content": item[2],

            "importance": item[3]

        }

        for item in data

    ]







# =========================
# 更新记忆
# =========================

def update_memory(
    memory_id,
    content,
    importance
):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        UPDATE memory


        SET


            content=?,


            importance=?,


            time=?


        WHERE id=?


        """,
        (
            content,

            importance,

            int(time.time()),

            memory_id

        )
    )


    conn.commit()

    conn.close()






# =========================
# 删除记忆
# =========================

def delete_memory(memory_id):

    conn = get_connection()

    cursor = conn.cursor()



    cursor.execute(
        """
        DELETE FROM memory

        WHERE id=?

        """,
        (
            memory_id,
        )
    )


    conn.commit()

    conn.close()





# =========================
# 自动初始化
# =========================

init_database()