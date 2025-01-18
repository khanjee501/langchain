from functools import partial
from .pinecone import build_retriver


retriever_map = {
    "pinecone_1": partial(
        build_retriver,
        k=1,
    ),
    "pinecone_2": partial(
        build_retriver,
        k=2,
    ),
    "pinecone_3": partial(
        build_retriver,
        k=3,
    ),
}
