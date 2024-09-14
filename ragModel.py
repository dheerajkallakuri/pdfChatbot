from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

api_key = "YOUR_API_KEY"

def get_pdf_content(documents):
    raw_text = ""

    for document in documents:
        pdf_reader = PdfReader(document)
        for page in pdf_reader.pages:
            raw_text += page.extract_text()

    return raw_text

def get_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_chunks = text_splitter.split_text(text)
    return text_chunks

def get_embeddings(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    vector_storage = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_storage

def start_conversation(vector_embeddings):
    llm = ChatOpenAI(openai_api_key=api_key)
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_embeddings.as_retriever(),
        memory=memory
    )
    return conversation

def get_conversation(pdf_text):
    chunks = get_chunks(pdf_text)
    vector_storage = get_embeddings(chunks)
    conversation = start_conversation(vector_storage)

    return conversation

def get_response(conversation,question):
    response = conversation.invoke(question)['answer']
    if response:
        return response
