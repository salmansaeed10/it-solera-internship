# import necessary laibraries
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Replace with your Groq API key
GROQ_API_KEY = "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"

# Chat groq model
model = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama-3.1-70b-versatile")

# Prompt template
template = """
Answer the question  below.

Here is the conversation history:{context}

Question: {question}

Answer: 
"""
prompt = ChatPromptTemplate.from_template(template)

#chain the model and prompt
chain = prompt | model

# heandle all conversation
def handle_conversation():
    context=""
    print("Welcome to the Ai chatbot, How may i help you! ")
    while True:
        user_input=input("User: ")

        # pass the chain to model
        result=chain.invoke({"context": context,"question":user_input})
        print("Bot: ",result.content)

        # saving data for context
        context=f"\nUser: {user_input}\nAI: {result.content}"

if __name__=="__main__":
    handle_conversation()
