from functools import partial
from .chatopenai import buil_llm

llm_map = {
    "gpt-4": partial(buil_llm, model_name="gpt-4"),
    "gpt-3.5-turbo": partial(buil_llm, model_name="gpt-3.5-turbo"),
}
