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
# 记忆合并判断
# =========================

def merge_memory(
    old_memory,
    new_memory
):


    prompt = f"""

你是一个长期记忆整理助手。

你的任务是帮助AI整理用户长期信息。


请判断下面两条记忆是否属于同一个用户信息。


旧记忆：

{old_memory}



新记忆：

{new_memory}



判断规则：

1. 如果两条记忆描述的是同一个兴趣、爱好、经历、习惯、目标或身份信息，则认为需要合并。

2. 即使文字表达不同，只要核心含义一致，也应该合并。

3. 如果新记忆是在补充旧记忆的信息，也应该合并。

例如：

旧：
喜欢洛天依

新：
喜欢洛天依三年，入坑曲是《天星问》

应该合并。


4. 只有完全无关的信息，才不要合并。



如果需要合并：

返回：

{{
    "merge": true,
    "content": "合并后的完整记忆"
}}



如果不需要合并：

返回：

{{
    "merge": false
}}



要求：

- 只返回JSON
- 不要输出解释
- 合并后的内容要简洁
- 保留所有重要信息


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

            "merge": False

        }