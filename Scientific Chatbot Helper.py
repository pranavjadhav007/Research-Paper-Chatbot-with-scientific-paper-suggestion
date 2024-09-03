import streamlit as st 

if "researchpaper_chatbot" not in st.session_state:
    from bot import Researchpaper_chatbot
    st.session_state.researchpaper_chatbot=Researchpaper_chatbot()

def generate_output(text):
    try:
        outp=st.session_state.researchpaper_chatbot.conversational_rag_chain.invoke({"input": text},
        config={
            "configurable": {"session_id": "abc123"}
        }, 
        )["answer"]
        return outp
    except:
        return "Sorry, I didn't understand that. Please try again."


st.title("Scientific Papers Helper Chatbot")

inp = st.chat_input("What the query?")


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


if inp:
    print("got in inp")
    st.session_state.chat_history.append({"role": "user", "response": inp})
    answer=generate_output(inp)
    print(answer)
    print("model ans end ")
    st.session_state.chat_history.append({"role": "chatbot", "response": answer})


for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(
            f"<span style='color:#4652DD; font-weight:bold;'>You: {chat['response']}</span>", 
            unsafe_allow_html=True
        )    
    else:
        st.write(f"Bot: {chat['response']}")







