import os
import openai


class OpenAIHelper:
    def __init__(self, openaiKey):
        self.openaiKey = openaiKey

    def answer(self, ques, option):
        openai.api_key = self.openaiKey
        conversation = [
            {
                "role": "system",
                "content": "你是一个中文答题机器人，你的能力是根据问题从几个选项中选出正确可能性最高的答案。你需要完整的打印出正确答案的文本，不需要提供任何解释。提供给你的问题可能存在错别字，返回结果时你需要将错别字纠正为正确的汉字。",
            }
        ]

        os.environ["http_proxy"] = "http://127.0.0.1:2080"
        os.environ["https_proxy"] = "http://127.0.0.1:2080"
        prompt = "问题:{};选项:{}.".format(ques, option)

        conversation.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            temperature=1,
            max_tokens=2048,
            top_p=0.9,
        )
        conversation.append(
            {
                "role": "assistant",
                "content": response["choices"][0]["message"]["content"],
            }
        )  # 将上一次会话信息返回给chatgpt
        print("\n" + response["choices"][0]["message"]["content"] + "\n")  # 打印答案
        return response["choices"][0]["message"]["content"]
