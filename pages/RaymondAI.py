import streamlit as st
import requests
import json
import db_call
import ollama_api
import asyncio
import pandas as pd
import dependency as dep
from config import config


ollama_url = ollama_api.ollama_url

################ <DIV> ################
model = config("LLM_MODEL", cast=str)
col1, col2 = st.columns([1,5])
with col1:
    st.image("images/mond.jpg", width=100)
with col2:
    st.title("raymondAI")
st.markdown("### Hello, I'm **Raymond** 🚀")

st.markdown(f"{dep.header}")
st.write(dep.brief_intro)

################ </DIV> ################


query = st.chat_input(placeholder="Ask me anything")
print(f"-->>> This is your query : {query}")


if query:
    with st.spinner("Generating SQL query..."):  # Show loading spinner
        gif_placeholder = st.empty()
        gif_placeholder.image("images/mond.gif", caption="Please wait...", use_container_width=True)

        request = {
            "model": model,
            "prompt": query,
            "stream": False,
        }
        # Make API request to Ollama
        response = requests.post(url=ollama_url.get("generate"), json=request)
        resp = response.json()

        gif_placeholder.empty()
        # Print full response
        orig_resp = resp.get("response")
        print("-->>> AI response : ", orig_resp)

        # Ensure response is valid JSON
        try:
            json_resp = json.loads(orig_resp)  # Parse JSON string into a dictionary
            print("JSON_RESP:", json_resp)
            sql_query = json_resp.get("sql", "No SQL query generated.")
            st.code(sql_query)  # Extract and put SQL query in GUI
            st.write(sql_query)
            db_data = asyncio.run(db_call.raw_query(sql_query))
            print("DB_DATA:", db_data)

            # Convert to DataFrame and display as table
            if db_data:
                df = pd.DataFrame(db_data)
                # Debug: Check if there's an extra unwanted column
                print("Columns before processing:", df.columns)
                # Ensure index column is removed
                df = df.reset_index(drop=True)
                # If an extra unwanted column exists, drop it
                if df.columns[0].lower() in ["index", "row_number"]:  # Adjust condition as needed
                    df = df.iloc[:, 1:]

                st.write("### Query Results:")
                st.dataframe(df.style.hide(axis="index"))  # Hide index explicitly
            else:
                st.warning("No data found for the given query.")




        except json.JSONDecodeError:
            print("Error: Response is not valid JSON")
            st.error("Error: AI response is not valid JSON")


