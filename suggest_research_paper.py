# DATA Reduce

import nltk
# nltk.download('punkt')
from dotenv import load_dotenv
load_dotenv()

import os

os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
os.environ["Gemini_API_key"] = os.getenv('Gemini_API_key')

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_groq import ChatGroq

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.google_palm import GooglePalmEmbeddings

class Suggest_research_paper_bot():

    model = ChatGroq(model="llama3-8b-8192")

    file_path = (
        "out_csdf_arxiv_db.csv"
    )

    loader = CSVLoader(file_path=file_path)
    data = loader.load()
    db=data[0:20]

    palm_embeddings=GooglePalmEmbeddings()

    datab = FAISS.from_documents(db, palm_embeddings)

    retriever_search = datab.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.runnables import RunnablePassthrough

    message = """
    Suggest the research paper based on the {context}.
    Only and only output the title of research paper.

    {question}

    """
    prompt_test = ChatPromptTemplate.from_messages([("human", message)])

    rag_chain = {"context": retriever_search, "question": RunnablePassthrough()} | prompt_test | model
