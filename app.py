import warnings
import torchvision

# Suppress warnings
torchvision.disable_beta_transforms_warning()
warnings.filterwarnings("ignore")

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disables GPU, forces CPU execution


import streamlit as st
import concurrent.futures
from dotenv import load_dotenv
import pdfplumber
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI 
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import HuggingFaceHub 
from htmlTemplates import css, bot_template, user_template

def extract_page_text(page):
    return page.extract_text() or ""  # Handle NoneType

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        with pdfplumber.open(pdf) as pdf_reader:  # ✅ Correctly opens streamlit file upload
            with concurrent.futures.ThreadPoolExecutor() as executor:
                pages_text = list(executor.map(extract_page_text, pdf_reader.pages))
            text += "\n".join(pages_text)
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    #embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    #llm = ChatOpenAI()
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-large",
        model_kwargs={"temperature": 0.7, "max_length": 1024}  # Increased from 512 to 1024
    )
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
    )
    return conversation_chain


def handle_userinput(user_question):
    if not user_question.strip():
        return  # Ignore empty questions

    if "chat_history" not in st.session_state or st.session_state.chat_history is None:
        st.session_state.chat_history = []

    if st.session_state.conversation is None:
        st.warning("⚠️ Please click 'Process' before asking questions.")
        return

    response = st.session_state.conversation({'question': user_question})

    # Ensure `response['chat_history']` exists before accessing it
    if response and 'chat_history' in response and response['chat_history']:
        if response['chat_history'][-1] not in st.session_state.chat_history:
            st.session_state.chat_history.extend(response['chat_history'][-2:])  # Only add latest exchanges

    # Display chat history
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
                       
    st.header("Chat with multiple PDFs by Aditya :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"): 
            with st.spinner("Processing"):
                 # Get the pdf text
                 raw_text = get_pdf_text(pdf_docs)

                 # Get the text chunks
                 text_chunks = get_text_chunks(raw_text)
                 
                 # Create vector store
                 vectorstore = get_vectorstore(text_chunks)

                 # create conversation chain
                 st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == "__main__":
    main()
