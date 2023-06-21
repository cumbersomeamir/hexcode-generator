import openai
import streamlit as st
from streamlit_chat import message
import re
import os
import json

count = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(prompt):

   prompt = "Give me a hexcode which matches with the following"


   completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": prompt}],
        functions=[
        {
            "name": "hexcode_generator",
            "description": "Generate hexcode which will go well with the entered hexcode or color",
            "parameters": {
                "type": "object",
                "properties": {
                    "hexcode": {
                        "type": "string",
                        "description" : "Generated Hexcode",
                        },
                    
                     "user_query": {
                        "type": "string",
                        "description": "Answers any question by the user"
                     }

                    }
                }
            }

        ],
        function_call= "auto",
)
   print("The completion is:", completion)
   arguments = json.loads(completion.choices[0].message.function_call["arguments"])
   print("The arguments are", arguments)
   message = arguments["hexcode"]
   #message = completion.choices[0].message.function_call["arguments"]["hexcode"]
   #print(message)
   return message

# EXECUTION OF THE PROGRAM STARTS HERE

st.title("Hexcode Generator")
st.info("Enter a color or hexcode to continue")


# Storing the chat

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

prompt = get_text()
print("The prompt is :", prompt)

if prompt:
    output = generate_response(prompt)
    # Save the output
    st.session_state.past.append(prompt)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        message(st.session_state['generated'][i], key = str(i))
        message(st.session_state['past'][i], is_user =True, key=str(i)+ '_user')
