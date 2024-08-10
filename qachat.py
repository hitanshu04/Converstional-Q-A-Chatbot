from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##function to load Gemini Pro Model and get response

model=genai.GenerativeModel("gemini-pro") #Initializing GenModel itself
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response


##initialize our streamlit app

st.set_page_config(page_title="Q&A Demo")

st.header("Gemini LLM Application")

##If I really want to record the history of converstaion we will initialize session state,so in streamlit it provides session states for chat history if doesn't exists

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]
    
    

input=st.text_input("Input:",key="input")
submit=st.button("Ask the question")

if submit and input:
    response=get_gemini_response(input)
    ## Add user query and respose to session chat history
    ## now here for all this entire history we are going ot save this in our chat_history session state
    st.session_state['chat_history'].append(("You",input))
    f=open("history.text","w")
    f.write(f"User input is : {input}\n")
    
    
    
    st.subheader("The response is")
    for chunk in response:
        st.write(chunk.text) #we r displaying text part by part
        st.session_state['chat_history'].append(("Bot",chunk.text))
        f.write(f"The output given by bot is :{chunk.text}\n")
        
        f.close()
st.subheader("The Chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
        
        
    
    



    


    
    
