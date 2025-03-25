import streamlit as st

st.title("Hello!! my name is Raymond, your Personal Assistant")

query = st.chat_input("Ask me anything")

st.chat_message("user").write(query)
st.chat_message("assistant").write("Hello!! my name is Raymond, your Personal Assistant")