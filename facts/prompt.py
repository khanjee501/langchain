from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import langchain
from dotenv import load_dotenv

langchain.debug = True

load_dotenv()

chat = ChatOpenAI()

embeddings = OpenAIEmbeddings()

db = Chroma(
    persist_directory="emb",
    embedding_function=embeddings,
)

retriever = db.as_retriever()

chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    # map rerank can also make up facts. It is almost identical to map_reduce. But one thing is that
    # it can give a similarity score as well through which it ranks the responses. So it is capable of
    # giving a response like no other chunk matches users query and can give it a score of 0. Or can even
    # give full score to an unrelated response. So has limitations.
    chain_type="map_rerank",
)

result = chain.run("What is an interesting fact about english language?")

print("\n")
print(result)
