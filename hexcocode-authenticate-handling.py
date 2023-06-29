import openai
import streamlit as st
from streamlit_chat import message
import re
import os
import json
from streamlit_credentials import get_credentials, login_required, User

count = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define your own function to check if a username/password combination is correct
def check_credentials(username, password):
    # In a real application, never store passwords in plain text!
    return username == 'admin' and password == 'password'

# This will show a login form until the user logs in
user = get_credentials()

# User is None if no one is logged in
if user is None:
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if username and password:
        if check_credentials(username, password):
            user = User(username)
            user.set_credentials()
        else:
            st.error('Invalid username or password')

@login_required
def main(user):
    st.title("Hexcode Generator")
    st.info("Enter a color or hexcode to continue")

    # Storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    def get_text():
        input_text = st.text_input("You: ", "", key="input")
        # Check if input is a valid hex code
        if re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', input_text):
            return input_text
        else:
            st.error('Invalid hex code. Please enter a valid hex code.')
            return None

    def generate_response(prompt):
        prompt = "Give me a hexcode which matches with the following"

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[{"role": "user", "content": prompt}],
                # rest of the parameters...
            )
        except Exception as e:
            st.error('An error occurred while generating a response. Please try again.')
            return None

        print("The completion is:", completion)
        arguments = json.loads(completion.choices[0].message.function_call["arguments"])
        print("The arguments are", arguments)
        message = arguments["hexcode"]
        #message = completion.choices[0].message.function_call["arguments"]["hexcode"]
        #print(message)
        return message

    # EXECUTION OF THE PROGRAM STARTS HERE

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

main(user)
