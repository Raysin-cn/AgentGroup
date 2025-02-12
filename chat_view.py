import streamlit as st
import json
import os

import streamlit_scrollable_textbox as stx
st.set_page_config(layout="centered", initial_sidebar_state="expanded")
# st.markdown("""
#         <style>
#                .block-container {
#                     padding-top: 1rem;
#                     padding-bottom: 0rem;
#                     padding-left: 30rem;
#                     padding-right: 30rem;
#                 }
#         </style>
#         """, unsafe_allow_html=True)


def chat_message_set(chat_id, user, avatar, message):
    with st.chat_message("user", avatar=avatar):
        st.markdown(user +"    "+ f"Time: {chat_id}")
        st.write(f"{message}")


characters_path = "/data/ll/LeiShijun/Gitclone/AgentGroup/storage/IsraeliPalestinianConflict_CH/initial_version/characters"
# characters_picture_path = "/data/ll/LeiShijun/Gitclone/AgentGroup/storage/icons"
# characters_picture = [characters_picture_path + "/" + i for i in os.listdir(characters_picture_path)]
characters_picture = {}
for i in os.listdir(characters_path):
    cha = json.load(open(characters_path + "/" + i, "r"))
    characters_picture[cha["id_name"]] = cha["portrait"]

history_path = "/data/ll/LeiShijun/Gitclone/AgentGroup/storage/IsraeliPalestinianConflict_CH/initial_version/action_history/0002.json"
op = open(history_path, "r")
history, chat_id = [], 1
for line in op:
    line_= json.loads(line)
    if line_["action_type"] == "### SAY":
        line_['id'] = chat_id
        chat_id += 1
        history.append(line_)

st.title("💬 AgentGroupChat")


tab1, tab2 = st.tabs(["📝 Chat History", "🤖 Main Characters"])




with tab2:
    for character in os.listdir(characters_path):
        info = json.load(open(os.path.join(characters_path, character), "r"))
        user = info['id_name']
        user_id = int(user.replace("C000", ""))
        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(info["name"]+'\n'+f"(C000{user_id})")
                st.image(characters_picture[user], caption=None, width=200)
            with col2:
                st.subheader("Scratch")
                st.write(info["scratch"])
                st.subheader("Background")
                st.write(info["background"])
            st.subheader("Objective")
            st.write(info["objective"])



with tab1:
    with st.sidebar:
        col1, col2 = st.columns(2)
        with col1:
            st.Start_message_id = int(st.text_input("Start message id", value=-20))
        with col2:
            st.End_message_id = int(st.text_input("End message id", value=len(history)))

    with st.container() as text:
        for chat_history in history[st.Start_message_id:st.End_message_id]:
            chat_id = chat_history["id"]
            user = chat_history["source_character_id_number"]
            user_id = int(user.replace("C000", ""))
            target_user = chat_history["to_character_id_number"]
            message = chat_history['action']
            message = message.replace(f"{user} say to {target_user}:", f"@{target_user}")
            chat_message_set(chat_id, user, characters_picture[user] , message)
            st.markdown(f"<br>", unsafe_allow_html=True)
    

print("END")