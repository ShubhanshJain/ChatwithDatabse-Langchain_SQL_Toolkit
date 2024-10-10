import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

st.set_page_config(page_title="  LangChain: Chat with SQL DB")
st.title("🦜 Langchain: Chat with SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "MY_SQL"

radio_opt = ["Use Local SQLLite 3 Database", "Connect to your SQL Database"]

selected_opt = st.sidebar.radio(label="Chose the DB which you want to chat", options=radio_opt)

if radio_opt.index(selected_opt) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MYSQl Host name")
    mysql_user = st.sidebar.text_input("MYSQL User")
    mysql_password = st.sidebar.text_input("MYSQL Password", type="password")
    mysql_db = st.sidebar.text_input("MYSQL Database")
else:
    db_uri = LOCALDB

api_key = st.sidebar.text_input(label="Enter Your GROQ API Key", type="password")

if not db_uri:
    st.warning("Please enter the database information and uri")

if not api_key:
    st.warning("Please enter the GROQ API Key")

# LLM Model:
llm = ChatGroq(api_key = api_key, model_name= "--ANY MODEL OF YOUR CHOICE--", streaming= True)

@st.cache_resource(ttl = "2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent/"--LOCAL DB NAME--").absolute()
        creator = lambda:sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri == MYSQL:
            if not(mysql_db and mysql_host and mysql_password and mysql_user):
                st.error("Please provide all MySQL connection details")
                st.stop()
            return SQLDatabase(create_engine(f"mysql+,ysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

if db_uri==MYSQL:
    db = configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db = configure_db(db_uri)

# ToolKit

toolkit = SQLDatabaseToolkit(db=db, llm = llm)
agent = create_sql_agent(llm=llm,toolkit=toolkit,verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

if "message" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["message"] = [{"role" : "assistant", "content" : "How can I help you?"}]

for msg in st.session_state.message:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input(placeholder = "Ask anything from database")

if user_query:
    st.session_state.message.append({"role":"user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        strealit_callback = StreamlitCallbackHandler(st.container())
        response = agent.run(user_query, callbacks = [strealit_callback])
        st.session_state.message.append({"role":"assistant", "content":response})
        st.write(response)