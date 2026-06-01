import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from app.config import settings

CHROMA_PATH = "./.chroma"

#preparacion del documento
async def process_pdf(file_path: str, filename: str):

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    return True


def format_docs(docs):

    return "\n\n".join(doc.page_content for doc in docs)

#fase de rag
async def generate_answer(question: str) -> str:

    embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(
        model="gpt-5.4-mini",
        openai_api_key=settings.OPENAI_API_KEY,
        temperature=0
    )

    system_prompt = (
        "Eres un asistente experto. Usa los siguientes fragmentos de contexto "
        "recuperado del documento para responder a la pregunta de forma precisa. "
        "Si no sabes la respuesta basándote en el contexto, di simplemente que no lo sabes, "
        "no intentes inventar la respuesta.\n\n"
        "Contexto:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])


    rag_chain = (
            {"context": retriever | format_docs, "input": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )


    response = rag_chain.invoke(question)

    return response