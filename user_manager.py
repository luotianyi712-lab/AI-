import re

from database import update_username



# =========================
# 自动提取用户名
# =========================

def extract_username(message):


    patterns = [

        r"我叫(.+)",

        r"我是(.+)",

        r"我的名字是(.+)",

        r"叫我(.+)"


    ]



    for pattern in patterns:


        result = re.search(
            pattern,
            message
        )


        if result:


            name = result.group(1)



            # 去掉多余符号

            name = name.strip()



            name = name.replace(
                "。",
                ""
            )


            name = name.replace(
                "！",
                ""
            )


            name = name.replace(
                "!",
                ""
            )



            if len(name) <= 20:


                return name



    return None





# =========================
# 更新用户昵称
# =========================

def check_username(
    user_id,
    message
):


    username = extract_username(
        message
    )


    if username:


        update_username(

            user_id,

            username

        )


        return username



    return None