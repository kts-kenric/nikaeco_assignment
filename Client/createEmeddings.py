from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import HuggingFaceBgeEmbeddings

def createEmbeddings():
    loader = DirectoryLoader('pdf',glob='./*.pdf',loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    texts = text_splitter.split_documents(documents)



    model_name = "BAAI/bge-base-en"
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

    model_norm = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cuda'},
        encode_kwargs=encode_kwargs
    )

    persist_directory = 'db'

    ## Here is the nmew embeddings being used
    embedding = model_norm

    vectordb = Chroma.from_documents(documents=texts,
                                    embedding=embedding,
                                    persist_directory=persist_directory)
