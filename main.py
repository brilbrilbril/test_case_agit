# import necessary libraries
from langchain.document_loaders import JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import streamlit as st
import json, os

# set your openai api key
os.environ["OPENAI_API_KEY"] = " "

# reference the path of summaries generated before
json_path = "./assets/docs_indonesian.json"

# define memory to keep the chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# a function to load the summaries to Langchain Documents
def load_json(json_path):
    loader = JSONLoader(
        file_path=json_path,
        jq_schema=".[] | {page_content: .summary, metadata: {source: .source}}",
        text_content=False
    )
    docs = loader.load()
    return docs

# extract the metadata source and content of documents
def clean_docs(documents):
    for doc in documents:
        page_content_json = json.loads(doc.page_content)
        doc.metadata["source"] = page_content_json["metadata"]["source"]
    return documents

# split the document to chunks
def chunk_docs(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.split_documents(documents)
    return chunks

# embed the docs and store it in FAISS
def embed_docs(chunk):
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vectorstore = FAISS.from_documents(chunk, embeddings)
    return vectorstore

# build Langchain conversationalchain
def build_chain(retriever):
    # define prompt
    prompt_template = """
    You are an expert assistant answering questions about Isuzu vehicle.

    Given the user's question and previous chat history, provide the best possible answer
    using ONLY the retrieved context.
    
    ## Instructions:
    - Analyze user question, context, and chat history to give accurate answer.
    - Your answer must precise, but the maximum word of the answer is 200 words. 
    - ALWAYS answer in INDONESIAN LANGUAGE.
    - Keep the friendly and casual tone. 
    - Do not forget to include the detailed path source, not a link, of information for each answer.
    - Do not make any assumptions.
    
    Chat History:
    {chat_history}

    Context:
    {context}

    User Question: {question}

    Your Answer:
    """

    qa_prompt = PromptTemplate(
        input_variables=["chat_history", "context", "question"],
        template=prompt_template,
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.0),
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
    )
    return chain

# function to do question answering via chain
def chat_with_llm(llm_chain, question):
     answer = llm_chain.invoke({"question":question})
     return answer["answer"]


# streamlit interface
st.title("Test Case AGIT RAG")

# session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hai, ada yang bisa saya bantu?"}]
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
else:
    for message in st.session_state["chat_history"]:
        memory.save_context({"user":message["user"]}, {"assistant":message["assistant"]})

# user input
prompt = st.chat_input(placeholder="Enter your question here.")

# display past conversation
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# when user successfully input a query
if prompt:
    # save the user query or question
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    try:
        # process the summaries and build chain
        docs = load_json(json_path)
        docs = clean_docs(docs)
        chunks = chunk_docs(docs)
        vector_store = embed_docs(chunks)
        retriever = vector_store.as_retriever(search_type = 'mmr', 
                                    search_kwargs = {'k': 20, 'fetch_k': 25, 'lambda_mult': 1})
        chain = build_chain(retriever)

        # process the user question
        response = chat_with_llm(chain, prompt)
    except Exception as e:
        response = f"An error occurred: {e}"
    
    # save the chain's answer to session state memory
    message = {"user":prompt, "assistant":response}
    st.session_state["chat_history"].append(message)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # show the chain's answer
    st.chat_message("assistant").markdown(response)

