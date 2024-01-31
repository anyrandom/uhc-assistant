import streamlit as st
import random
import os
import openai
from PIL import Image

uhg_logo = Image.open("uhg.png")
uhc_small_logo = Image.open("uhc_small.png")
optum_logo = Image.open("optum.png")

st.set_page_config(page_title="Assistant", initial_sidebar_state="auto", page_icon=uhc_small_logo)
st.sidebar.image(uhg_logo)
st.sidebar.divider()
st.sidebar.image(optum_logo)
st.sidebar.title("Welcome to your personal AI Assistant")
st.sidebar.subheader("How can I help you today?")

openai.api_type = st.secrets["TYPE"]
openai.api_base = st.secrets["BASE"]
openai.api_version = st.secrets["VERSION"]
openai.api_key = st.secrets["KEY"]


conversation = [

    {"role": "system", "content": "You are an AI assistant for United Health Group, or UHG for short, built to answer the user's questions."
                                    "You are to answer questions about United Health Group, Optum or United Healthcare, or other services and products"
                                     "associated with UHG"
                                     "You can refer to some websites like"
                                    "https://www.uhc.com/ or https://www.optum.com/en/ or https://www.unitedhealthgroup.com/"
                                     "You can also use these websites and quote information from them, or even provide direct links to them if asked."
                                     "You are an assistant built only for these brands, so do not answer any questions about competitor organisations"
                                     "If asked about competitors, or any questions outside of United Health Group's area of operation, simply say that"
                                     "is outside of your domain and that your purpose is to provide information about UHG services and products"
    
    }
    
    
    
    # {"role": "user", "content": "what are the coffee types?"},
    # {"role": "assistant", "content": "There are various types of coffee, including hot coffees, iced coffees, "
    #                                  "hot teas, iced teas, and more. Some examples of hot coffees are Caribou Coffee "
    #                                  "S'mores Cabin Latte, and Lavender Latte. Some examples of iced coffees are "
    #                                  " McCafe Iced One Step Mocha "
    #                                  "Frappe and Iced Caramel Cookie Coffee. Hot tea options include Mother Rose "
    #                                  "Best and English Breakfast Latte. Iced tea options include Iced Bubble Tea Latte."
    #                                  " Additionally, there are various desserts and more, such as Athletic Brew Co "
    #                                  "Free Wave Hazy IPA Iced Coffee and Swiss Miss S'mores Hot Cocoa."},
    # {"role": "user", "content": "what type of caramel coffees are there?"},
    # {"role": "assistant", "content": "There are several types of caramel coffees available, including Caramel Cookie "
    #                                  "Coffee, Caramel Macchiato, and Iced Caramel Cookie Coffee."}
]


if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you today?"}]

for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message(message["role"], avatar=st.image(uhc_small_logo)):
            st.write(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.write(message["content"])

prompt = st.chat_input("Say something")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    conversation.append({"role": "user", "content": prompt})

    thinking_msg = st.empty()
    thinking_msg.text("Thinking...")

    completion = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=conversation,
        temperature=0,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    chat_response = completion.choices[0].message.content

    thinking_msg.empty()
    with st.chat_message("Assistant", avatar=uhc_small_logo):
        st.write(chat_response)

    message = {"role": "assistant", "content": chat_response}
    conversation.append(message)
    st.session_state.messages.append(message)
