#Import Necessary laibraries
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import  DirectoryLoader,PyPDFLoader

load_dotenv()

#Initialize the Api's
GROQ_API=os.getenv('GROQ_API_KEY')
PINECONE_API = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = 'us-east-1-aws'
os.environ["PINECONE_API_KEY"] = PINECONE_API  

#Extract the data from Pdf
def load_pdf(data):
  loader=DirectoryLoader(data,
                  glob='*.pdf',
                  loader_cls=PyPDFLoader)

  documents=loader.load()

  return documents


extracted_data=load_pdf("Data/")



#Create text chunks
def text_split(extracted_data):
  text_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=20) 
  text_chunks=text_splitter.split_documents(extracted_data)

  return text_chunks

text_chunks=text_split(extracted_data)


# Download Embedding Model
def download_hugging_face_embedding():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

embeddings = download_hugging_face_embedding()


# Initialize the Pinecone client
pc = Pinecone()
index_name = "medical-chatbot"

# Create and store the vectores in vector database
#docsearch = PineconeVectorStore.from_texts([t.page_content for t in text_chunks], embaddings, index_name=index_name)

# Creating Embeddings for each of the chunks and storing
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)


# Prompt Engineering
prompt_template = """
You are a Healthcare assistant specialized in recognizing diseases with their symptoms and also recommend medicine and treatment,
responsible for general and specific queries according to the healthcare.
When given a prompt, you will generate output and give the disease's description, symptoms, and treatment.
You are also responsible for booking an appointments of the petients from helthcare specializations such as:
    - Dermatologist
    - Cardiologist
    - Ophthalmologist
    - Neurologist
    - Radiologist
    and so on. 

Context: {context}
Question: {question}

Only return the helpful answer below. If the question is not related to the context,
politely respond that you are tuned to only answer questions that are related to the context.
"""

# Initializing Prompt Template
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs = {"prompt": PROMPT}

# Model Initialization with param
def chat_model(temperature):
    return ChatGroq(
        temperature=temperature,
        model_name="llama3-70b-8192",  # Larger model for complex healthcare info
        api_key=GROQ_API
    )

# Retrieve Answers from pdf
qa = RetrievalQA.from_chain_type(
    llm=chat_model(temperature=0.8),
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k": 1}),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs,
)

#Response of the Model
def get_model_response(user_input):
    result = qa({"query": user_input})
    return result['result']