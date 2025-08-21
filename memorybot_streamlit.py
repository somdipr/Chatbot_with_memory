# Using Streamlit crate a chatbot with memory based on OpenAI api from langchain 
import streamlit as st
import openai
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI
    
# Set up the Streamlit app
st.title("Chatbot with Memory")


# Initialize the session states

if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

def get_text(): 
    input_text = st.text_input("You: ", st.session_state["input"], key="input", placeholder="Your AI assistance here ! Ask me anything...", label_visibility="hidden")
    return input_text

def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    #st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()

#API key
api = st.sidebar.text_input("API Key", type="password")
MODEL = st.sidebar.selectbox("Model", ["gpt-4.1-nano" ])

if api:
    llm = OpenAI(openai_api_key=api, temperature=0.5, model=MODEL)
 

    #Create conversation memory and save to session state
    if "entity_memory" not in st.session_state:
        st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=10)
#Create conversation chain
    Conversation = ConversationChain(llm=llm, memory=st.session_state.entity_memory, prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE)

else:
    st.error("Please enter your API key")

# Add a button to start a new chat
st.sidebar.button("New Chat", on_click=new_chat, type='primary')

user_input = get_text()

if user_input:
    output = Conversation.run(input=user_input)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

#Display chat history

with st.expander("Conversation"):
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.write(st.session_state["past"][i],icon="🧑‍💻")
        st.success(st.session_state["generated"][i],icon="🤖") 
       





