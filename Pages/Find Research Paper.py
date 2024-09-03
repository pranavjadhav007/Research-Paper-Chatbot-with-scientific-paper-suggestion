import streamlit as st

if "suggestion_bot" not in st.session_state:
    from suggest_research_paper import Suggest_research_paper_bot
    st.session_state.suggestion_bot = Suggest_research_paper_bot()

st.title("Find the similar Research papers")

inpu=st.text_input("Enter the related keyword. ")

if inpu:
    response = st.session_state.suggestion_bot.rag_chain.invoke(inpu)
    st.write("Below are the suggested research Papersz: ")
    st.write(response.content)