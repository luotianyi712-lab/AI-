from openai import OpenAI
import os
import json


API_KEY = os.getenv("API_KEY")

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



def extract_memory(message):

    prompt = f"""

你是一个记忆提取助手。

请分析用户的话，判断是否有值得长期记忆的信息。

只保存：
- 用户长期兴趣
- 用户喜欢的事物
- 用户重要经历
- 用户长期目标
- 用户习惯

不要保存：
- 临时聊天
- 一次性的情绪
- 普通寒暄


用户消息：

{message}


如果没有重要信息，返回：

{{"save":false}}


如果有，返回 JSON：

{{
"save":true,
"type":"类型",
"content":"记忆内容",
"importance":1-5
}}

只输出JSON，不要解释。

"""


    response = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]

    )


    text=response.choices[0].message.content


    try:

        return json.loads(text)

    except:

        return {
            "save":False
        }