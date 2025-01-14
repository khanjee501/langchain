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
    llm=chat, retriever=retriever, chain_type="map_reduce"
)

result = chain.run("What is an interesting fact about english language?")

print("\n")
print(result)
