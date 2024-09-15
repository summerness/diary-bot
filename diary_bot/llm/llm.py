import time

import markdown
from dashscope import MultiModalConversation
import dashscope
from diary_bot.config.settings import settings
from openai import OpenAI


class QwenVLService:
    def __init__(self):
        dashscope.api_key = settings.ALI_TOKEN
        self.prompt1 = settings.PROMPT1
        self.prompt2 = settings.PROMPT2
        self.prompt3 = settings.PROMPT3
        self.prompt4 = settings.PROMPT4
        self.client = OpenAI(
            api_key=settings.ALI_TOKEN,  # 替换成真实DashScope的API_KEY
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope服务endpoint
        )

    def call_text(self, messages, retry_count=0):
        # 设置最大重试次数
        max_retries = 5
        completion = self.client.chat.completions.create(
            model="qwen-long",
            messages=messages,
            stream=False
        )
        if len(completion.choices) > 0:
            generated_text = completion.choices[0].message.content
            print(generated_text)
            time.sleep(61)

            return generated_text
        else:
            # 如果请求失败且重试次数少于最大重试次数，递归调用自己
            if retry_count < max_retries:
                print("retrying", retry_count)
                time.sleep(60 * (retry_count + 1))  # 等待61秒再重试
                return self.call_text(messages, retry_count + 1)
            else:
                # 超过最大重试次数，返回 None
                return None

    def call(self, messages, retry_count=0):
        # 设置最大重试次数
        max_retries = 5

        responses = MultiModalConversation.call(
            model='qwen-vl-plus',
            messages=messages,
            stream=False
        )

        # 检查 responses 是否包含有效的输出
        if responses and responses.get("output") and "choices" in responses["output"]:
            generated_text = responses["output"]["choices"][0]["message"]["content"][0]["text"]
            print(generated_text)
            time.sleep(61)

            return generated_text
        else:
            # 如果请求失败且重试次数少于最大重试次数，递归调用自己
            if retry_count < max_retries:
                print("retrying", retry_count)
                time.sleep(60 * (retry_count + 1))  # 等待61秒再重试
                return self.call(messages, retry_count + 1)
            else:
                # 超过最大重试次数，返回 None
                return None

    def multimodal_conversation_call(self, images):
        texts = []
        messages = []

        for index, image in enumerate(images):
            image = image.get('links').get('thumbnail_url')
            if index == 0:
                user_message = {
                    "role": "user",
                    "content": [
                        {"image": image},
                        {"text": self.prompt1}
                    ]
                }
            else:
                user_message = {
                    "role": "user",
                    "content": [
                        {"image": image},
                        {"text": self.prompt2}
                    ]
                }

            messages.append(user_message)
            generated_text = self.call(messages)
            if generated_text:
                assistant_message = {
                    "role": "assistant",
                    "content": [{"text": generated_text}]
                }
                messages.append(assistant_message)
                texts.append(generated_text)

        generated_text = self.call_text([{
            "role": "user",
            "content": "{}\n,{}".format(self.prompt3, "\n".join(texts))
        }])
        texts.append(generated_text)
        title = self.call([{
            "role": "user",
            "content": [
                {"text": "{}\n,{}".format(self.prompt4, "\n".join(texts))}
            ]
        }])

        return texts, title.lstrip('#').lstrip()
