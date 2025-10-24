import json

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()


class Recipe(BaseModel):
    ingredients: list[str] = Field(description="料理の材料")
    steps: list[str] = Field(description="料理の作り方")


client = OpenAI()

with client.chat.completions.stream(
    model="gpt-5-nano",
    reasoning_effort="minimal",
    messages=[{"role": "user", "content": "カレーのレシピを考えて"}],
    response_format=Recipe,
) as stream:
    for event in stream:
        if hasattr(event, "parsed") and event.parsed is not None:
            print(json.dumps(event.parsed, ensure_ascii=False), flush=True)
