"""Module providing Function Enabling multi-round conversations with azure OPENAI."""

import os
import openai
from dotenv import load_dotenv

# 从.env文件中读取API设置和密钥
load_dotenv(dotenv_path='.env')
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

# 初始化会话
messages = [{"role": "system", "content": "You are a helpful assistant."}]

while True:
    # 获取用户输入
    user_input = input("You: ")

    # 添加用户消息到会话
    messages.append({"role": "user", "content": user_input})

    # 构建请求
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=messages
    )

    # 获取AI回复
    ai_message = response.choices[0].message
    ai_output = ai_message["content"]

    # 输出回复
    print("AI:", ai_output)

    # 添加AI消息到会话
    messages.append({"role": "assistant", "content": ai_output})

    # 检查是否退出
    if user_input.lower() == "exit":
        break
