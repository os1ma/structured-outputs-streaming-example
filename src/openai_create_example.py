import json

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()


class Recipe(BaseModel):
    ingredients: list[str] = Field(description="料理の材料")
    steps: list[str] = Field(description="料理の作り方")


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5-nano",
    reasoning_effort="minimal",
    messages=[{"role": "user", "content": "カレーのレシピを考えて"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "Recipe",
            "schema": {
                **Recipe.model_json_schema(),
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    stream=True,
)

output_parser = JsonOutputParser()

content = ""
for chunk in response:
    if len(chunk.choices) == 0:
        continue
    chunk_content = chunk.choices[0].delta.content
    if chunk_content:
        content += chunk_content
        parsed_content = output_parser.invoke(content)
        print(json.dumps(parsed_content, ensure_ascii=False), flush=True)
