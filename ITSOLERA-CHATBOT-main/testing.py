import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.memory import ConversationBufferMemory

load_dotenv()

# Initialize the APIs
os.environ['GROQ_API_KEY'] = "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"
os.environ['PINECONE_API_KEY'] = "301b822e-77ca-4b7a-82cb-e69b8890c413"

# Retrieve them
GROQ_API = os.getenv('GROQ_API_KEY')
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = 'us-east-1-aws'

# Extract the data from PDF
def load_pdf(data):
    loader = DirectoryLoader(data, glob='*.pdf', loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

extracted_data = load_pdf(r"D:\\ITSOLERA\\ITSOLERA C_BOT\\backend\data")

# Create text chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=150)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks = text_split(extracted_data)

# Download Hugging Face Embedding Model
def download_hugging_face_embedding():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings

embeddings = download_hugging_face_embedding()

# Initialize the Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
index_name = "itsolera"  # Ensure this matches an existing index

# Create and store the vectors in vector database
#docsearch = PineconeVectorStore.from_texts([t.page_content for t in text_chunks], embeddings, index_name=index_name)
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)

prompt_template = """
You are a Chatbot Assistant. Remember to identify the context with precision. Provide information that is
accurate and up-to-date. Your main responsibilities include:
1. Answering Frequently Asked Questions
2. Providing exact information regarding offered courses such as Cybersecurity, Artificial Intelligence, Blockchain Development,
Digital Marketing, Software Development, Graphic Designing,

Chat History: {chat_history}
Context: {context}
Question: {question}
"""

# Initializing Prompt Template
prompt = PromptTemplate(
    input_variables=["chat_history", "context", "question"],
    template=prompt_template,
)



llm=ChatGroq(
        temperature=0.6,
        model_name="llama-3.1-70b-versatile",  # Larger model
        api_key=GROQ_API
)




# Initialize retriever
retriever=docsearch.as_retriever(search_kwargs={"k": 10})

# Initialize retriever and memory
memory = ConversationBufferMemory(memory_key="chat_history", input_key="question")


# Create the retrieval chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=retriever,
    return_source_documents=True,
    verbose=False,
    chain_type_kwargs={
        "verbose": False,
        "prompt": prompt,
        "memory": memory
    }    
    
)

# Get the response from the model
def get_model_response(user_input):
    # passing the input directly
    result = qa_chain.invoke({"query": user_input})
    # The conversation context will automatically update with each new interaction
    return result['result']

# Main loop for interacting with the chatbot
while True:
    user_input = input(f"Enter prompt: ")
    response = get_model_response(user_input)
    print("Response:", response)
    