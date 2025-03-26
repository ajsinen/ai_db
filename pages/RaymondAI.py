import streamlit as st
import requests
import json
import db_call
import asyncio

model = "raymond"
col1, col2 = st.columns([1,5])
with col1:
    st.image("image.jpg", width=50)
with col2:
    st.title("raymondAI")
st.write("Hello I'm raymond, your personal Database Administrator")
ollama_url = {
    "generate": "http://localhost:11434/api/generate",
    "chat": "http://localhost:11434/api/chat",
}

# Initialize session state for query processing
if "processing" not in st.session_state:
    st.session_state.processing = False

query = st.chat_input(placeholder="Ask me anything", disabled=st.session_state.processing)
print(f"-->>> This is your query : {query}")

if query:
    # Set processing state to True (disables input)
    st.session_state.processing = True


if st.session_state.processing:
    with st.spinner("Generating SQL query..."):  # Show loading spinner
        request = {
            "model": model,
            "prompt": query,
            "stream": False,
        }
        response = requests.post(url=ollama_url.get("generate"), json=request)
        resp = response.json()

        # Print full response
        orig_resp = resp.get("response")
        print("-->>> AI response : ", orig_resp)

        # Ensure response is valid JSON
        try:
            json_resp = json.loads(orig_resp)  # Parse JSON string into a dictionary
            print("JSON_RESP:", json_resp)
            sql_query = json_resp.get("sql", "No SQL query generated.")
            print("SQL:", sql_query)  # Extract and print the SQL query
            st.write(sql_query)
            db_data = db_call.call_db(sql_query)
            print("DB_DATA:", db_data)

        except json.JSONDecodeError:
            print("Error: Response is not valid JSON")
            st.error("Error: AI response is not valid JSON")

    # Reset processing state after completion
    st.session_state.processing = False
    st.rerun()  # Refresh UI to re-enable input

