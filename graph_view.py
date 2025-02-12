# Currently not workin since update to agraph 2.0 - work in progress
from rdflib import Graph
from streamlit_agraph.config import Config, ConfigBuilder
from streamlit_agraph import agraph, Node, Edge, Config
import streamlit as st
import os
import json
import math

nodes = []
edges = []
graph = Graph()


if 'id_step' not in st.session_state:
    st.session_state.id_step = 0
if 'hightlight_edge' not in st.session_state:
    st.session_state.hightlight_edge = None

characters_path = "/data/ll/LeiShijun/Gitclone/AgentGroup/storage/succession/test_version/characters"
characters_file = os.listdir(characters_path)
history_path = "/data/ll/LeiShijun/Gitclone/AgentGroup/storage/succession/test_version/action_history/0000.json"

op = open(history_path, "r")
history = []
for line in op:
    history.append(line)

def click_step(direction):
    if direction == "right":
        st.session_state.id_step += 1
    elif direction == "left":
        st.session_state.id_step -= 1
    elif direction == "reset":
        st.session_state.id_step = 0
    

def character_to_node(json_file:str, node_condinate:tuple):
    op = open(json_file, 'r')
    data = json.load(op)
    return(Node(id = data['id_name'],
                label = data['id_name'],
                image = "/data/ll/LeiShijun/Gitclone/AgentGroup/streamlit/robot.png",
                size = 20 if data['main_character'] else 10,
                x = node_condinate[0],
                y = node_condinate[1],
               ))

def history_to_edge(json_dict:dict):
    return Edge(id = json_dict['id'],
                source = json_dict["source_character_id_number"],
                label = json_dict["action_type"].split("###")[-1],
                target = json_dict["to_character_id_number"],
                title = json_dict["action"].split("###")[-1]
            )

def load_node(characters_path:str, characters:list):
    nodes_num = len(characters)
    center_point = (200, 200)
    diameters = 200
    nodes_condinate = [(center_point[0] + diameters * math.cos(2 * math.pi * i / nodes_num),
                        center_point[1] + diameters * math.sin(2 * math.pi * i / nodes_num))
                        for i in range(nodes_num)]

    for i, c in enumerate(characters):
        nodes.append(character_to_node(characters_path + '/' + c, nodes_condinate[i]))
        # print(f"load character {c}")


def load_edge(history:list, id_sta, id_end):
    for line in history[id_sta:id_end+1]:
        json_dict = json.loads(line)
        edges.append(history_to_edge(json_dict))
        print(f"load edge {json_dict['id']}")


def reset_graph(edge_id, history=history):
    if edge_id != None:
        global edges
        edges = []
        edges.append(history_to_edge(json.loads(history[edge_id])))

def info_swarm(history:list, id_sta, id_end):
    st.subheader("交互流信息")
    hightlight_select = False
    for line in history[id_sta:id_end+1]:
        json_dict = json.loads(line)
        info_extend = st.button(f"""id: *{json_dict['id']:3}*  {json_dict['source_character_id_number']} >> {json_dict['to_character_id_number']}    {json_dict['action_type'].split("###")[-1]} """, key=f"{json_dict['id']}")
        if info_extend:
            st.write(f"{json_dict['action']}")
            st.session_state.hightlight_edge = json_dict['id']
            hightlight_select = True
    if hightlight_select == False:
        st.session_state.hightlight_edge = None


def comment_set():
    col1, col2, col3 = st.columns(3,)
    with col1:
        id_step_len = int(st.text_input("步长", value=1))-1
        st.button("重置偏移量", on_click = click_step, args=["reset"])  
    with col2:
        # id_sta = st.silder('起始时间戳', min_value=0, max_value=len(history), value=0) + st.session_state.id_step
        id_sta = int(st.text_input("起始时间戳", value=0)) + st.session_state.id_step
        st.button("向左一步", on_click = click_step, args=["left"])
    with col3:
        # id_end = st.silder('终止时间戳', min_value=0, max_value=len(history), value=0) + st.session_state.id_step
        id_end = max(int(st.text_input("终止时间戳", value=id_sta-st.session_state.id_step)) + st.session_state.id_step , id_sta) + id_step_len
        st.button("向右一步", on_click = click_step, args=["right"])

    with col1:
        st.write(f"步长偏移量：{st.session_state.id_step}")
    with col2:
        st.write(f"开始：{id_sta}")
    with col3:
        st.write(f"结束：{id_end}")
    return id_sta, id_end



# config = Config(width=500, 
#                 height=500, 
#                 directed=True,
#                 nodeHighlightBehavior=True, 
#                 highlightColor="#F7A7A6", # or "blue"
#                 collapsible=True,
#                 time_step=0.1,
#                 node={'labelProperty':'label'},
#                 link={'labelProperty': 'label', 'renderLabel': True},
#                 staticGraphWithDragAndDrop=True
#                 # **kwargs e.g. node_size=1000 or node_color="blue"
#                 )

config = Config(from_json="/data/ll/LeiShijun/Gitclone/AgentGroup/streamlit/config.json")
config_builder = ConfigBuilder(nodes)
config = config_builder.build()
# config.save("streamlit/config.json")

st.title("AgentGroup")
load_node(characters_path, characters_file)
id_sta, id_end = comment_set()
load_edge(history, id_sta, id_end)
info_swarm(history, id_sta, id_end)
reset_graph(st.session_state.hightlight_edge)
return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)



print("END")