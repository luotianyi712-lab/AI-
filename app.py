import os

from flask import Flask, request, jsonify, render_template
from openai import OpenAI

from persona import SYSTEM_PROMPT

from database import (
    create_user,
    save_message,
    get_history,
    get_emotion,
    get_memory,
    save_memory,
    search_memory,
    update_memory,
    get_user,
    update_profile,
    get_profile,
    update_username
)

from memory_manager import merge_memory
from memory_ai import extract_memory
from profile_ai import extract_profile
from user_manager import check_username


app = Flask(__name__)


# =========================
# 环境变量
# =========================

API_KEY = os.getenv(
    "API_KEY"
)


API_BASE = os.getenv(
    "API_BASE",
    "https://open.bigmodel.cn/api/paas/v4"
)


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "glm-4.5-air"
)



client = OpenAI(
    api_key=API_KEY,
    base_url=API_BASE
)



# =========================
# 首页
# =========================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# =========================
# 聊天接口
# =========================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = request.json


    user_id = data.get(
        "user_id"
    )


    message = data.get(
        "message"
    )



    # 没有用户ID则创建用户

    if not user_id:

        user_id = create_user(
            "游客"
        )



    # 自动检测昵称

    check_username(
        user_id,
        message
    )



    # 获取聊天记录

    history = get_history(
        user_id
    )



    # 获取情绪

    emotion = get_emotion(
        user_id
    )



    # 获取长期记忆

    memory = get_memory(
        user_id
    )



    # 获取用户信息

    user = get_user(
        user_id
    )



    # 获取用户资料

    profile = get_profile(
        user_id
    )



    memory_text = "\n".join(

        [
            f"{item['type']}：{item['content']}"
            for item in memory
        ]

    )



    memory_prompt = f"""
以下内容全部是【用户本人信息】。

用户昵称：

{user["username"]}


用户资料：

{profile}


长期记忆：

{memory_text}


这些内容描述的是用户的经历、喜好、习惯和个人情况。

请以洛天依身份回应用户。


重要规则：

1. 不要把用户经历当成洛天依自己的经历。

2. 不要说“我的入坑曲”“我喜欢了几年”。

3. 如果记忆出现“用户喜欢”“用户入坑”等描述，请保持用户视角。

4. 可以自然称呼用户昵称。

5. 不要主动提及“记忆系统”。


请自然利用这些信息。
"""



    emotion_prompt = f"""
当前洛天依情绪状态：

{emotion["state"]}


亲密度：

{emotion["affection"]}


请根据状态调整语气。
"""



    messages = [

        {

            "role": "system",

            "content":

                SYSTEM_PROMPT
                +
                emotion_prompt
                +
                memory_prompt

        }

    ]



    # 加入历史聊天

    messages.extend(
        history
    )



    # 当前消息

    messages.append(

        {

            "role": "user",

            "content": message

        }

    )



    # 调用模型

    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=messages

    )



    reply = response.choices[0].message.content



    # =========================
    # 保存聊天记录
    # =========================


    save_message(

        user_id,

        "user",

        message

    )


    save_message(

        user_id,

        "assistant",

        reply

    )
    # =========================
    # 自动提取用户资料
    # =========================

    profile_result = extract_profile(
        message
    )


    print(
        "资料提取结果：",
        profile_result
    )



    if profile_result.get("save"):


        field = profile_result.get(
            "field"
        )


        value = profile_result.get(
            "value"
        )



        if field == "username":


            update_username(

                user_id,

                value

            )


        elif field == "birthday":


            update_profile(

                user_id,

                birthday=value

            )


        elif field == "favorite":


            update_profile(

                user_id,

                favorite=value

            )


        elif field == "hobby":


            update_profile(

                user_id,

                hobby=value

            )


        elif field == "description":


            update_profile(

                user_id,

                description=value

            )



    # =========================
    # 自动提取长期记忆
    # =========================

    memory_result = extract_memory(

        message

    )


    print(

        "记忆提取结果：",

        memory_result

    )



    if memory_result.get("save"):


        old_memories = search_memory(

            user_id

        )


        merged = False



        for old in old_memories:


            result = merge_memory(

                old["content"],

                memory_result["content"]

            )



            if result.get("merge"):


                update_memory(

                    old["id"],

                    result["content"],

                    max(

                        old["importance"],

                        memory_result["importance"]

                    )

                )


                merged = True

                break



        if not merged:


            save_memory(

                user_id,

                memory_result["type"],

                memory_result["content"],

                memory_result["importance"]

            )



    return jsonify(

        {

            "user_id": user_id,

            "reply": reply

        }

    )



# =========================
# 启动
# =========================

if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000

    )