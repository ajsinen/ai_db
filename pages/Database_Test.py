import asyncio

import config
import db_call
import streamlit as st


data = asyncio.run(db_call.raw_query("SELECT * FROM staff"))
print("DATABASE RESULT: ",data)
st.write(data[0].keys())

