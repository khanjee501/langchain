from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from redundant_filter_retriever import RedundantFilterRetriever
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

# retriever = db.as_retriever()

retriever = RedundantFilterRetriever(
    embeddings=embeddings,
    chroma=db,
)

chain = RetrievalQA.from_chain_type(
    llm=chat,
    retriever=retriever,
    # reverting back to stuff as it will be the most commonly used and has better results in almost
    # ost of the cases. It is cheap compared to other chain types as it call chains less than the other types.
    # the others may be well suited for advanced or specialized cases but dont use them if not required.
    chain_type="stuff",
)

result = chain.run("What is an interesting fact about english language?")

print("\n")
print(result)
