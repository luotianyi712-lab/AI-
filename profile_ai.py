import os
import json

from openai import OpenAI



# =========================
# AI连接
# =========================

client = OpenAI(

    api_key=os.getenv("API_KEY"),

    base_url=os.getenv(
        "API_BASE",
        "https://open.bigmodel.cn/api/paas/v4"
    )

)



MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "glm-4.5-air"
)





# =========================
# 自动提取用户资料
# =========================

def extract_profile(message):


    prompt = f"""

你是一个用户资料提取助手。

请分析下面这句话。

用户消息：

{message}



如果里面包含用户固定资料，请提取。



可提取字段：

username:
用户昵称


birthday:
生日


favorite:
喜欢的人、角色、作品、歌曲


hobby:
兴趣爱好


description:
其他长期个人信息




如果发现资料：

只返回JSON：

{{
    "save": true,
    "field": "字段名",
    "value": "内容"
}}



如果没有资料：

返回：

{{
    "save": false
}}



要求：

1. 只能返回JSON

2. 不要解释

3. 不要猜测不存在的信息

4. 必须是用户自己的信息


"""


    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[

            {

                "role": "user",

                "content": prompt

            }

        ]

    )



    result = response.choices[0].message.content



    try:

        return json.loads(
            result
        )


    except Exception:


        return {

            "save": False

        }