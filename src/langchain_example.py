from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

load_dotenv()


class Recipe(TypedDict):
    ingredients: Annotated[list[str], ..., "料理の材料"]
    steps: Annotated[list[str], ..., "料理の作り方"]


model = init_chat_model(
    model_provider="openai",
    model="gpt-5-nano",
    reasoning_effort="minimal",
)

model_with_structure = model.with_structured_output(Recipe, method="json_schema")

for chunk in model_with_structure.stream("カレーのレシピを考えて"):
    print(chunk, flush=True)
