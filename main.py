import os
import json
from openai import OpenAI
client = OpenAI(
    api_key="xxxxx",
    base_url="https://api.chatanywhere.tech"
)

conversation = [{"role": "system", "content": "你是一个助手，帮助用户构建数据集。"},
                {"role": "system", "content": '对于用户发过来的信息，你要像这样回答：{"chosen": "优质回答（必填）","rejected": "劣质回答（必填）"}'}]

result_list = []

with open(file='data.jsonl', mode='r', encoding='utf-8') as file:
    data = json.load(file)
    index = 0
    for message in data:
        if index == 1:
            break
        current_conversation = conversation.copy()
        print(message["question"])
        current_conversation.append({"role": "user", "content": message["question"]})
        response = client.chat.completions.create(
            messages=current_conversation,
            model="gpt-4o-ca"
        )
        response_dict=json.loads(response.choices[0].message.content)
        result_list.append({
                "instruction": message["question"],
                "chosen": response_dict["chosen"],
                "rejected": response_dict["rejected"]
            })
        index += 1

with open('dpo_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(result_list, f, ensure_ascii=False, indent=2)