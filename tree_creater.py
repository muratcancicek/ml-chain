import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import json
import time

DEGEN_AIRDROP_FOLDER = 'data/graph10-100-01'

def read_parent_transactions(degree):
    received_path = f'{DEGEN_AIRDROP_FOLDER}/degree_{degree}_parent_received.json'
    received = json.load(open(received_path, 'r'))
    sent_path = f'{DEGEN_AIRDROP_FOLDER}/degree_{degree}_parent_sent.json'
    sent = json.load(open(sent_path, 'r'))
    return received, sent

def read_child_transactions(degree):
    received_path = f'{DEGEN_AIRDROP_FOLDER}/degree_{degree}_child_received.json'
    received = json.load(open(received_path, 'r'))
    sent_path = f'{DEGEN_AIRDROP_FOLDER}/degree_{degree}_child_sent.json'
    sent = json.load(open(sent_path, 'r'))
    return received, sent

def read_degree_transactions(degree):
    received_path = f'{DEGEN_AIRDROP_FOLDER}/degree_{degree}_received.json'
    received = json.load(open(received_path, 'r'))
    sent_path = f'{DEGEN_AIRDROP_FOLDER}/degree_{degree}_sent.json'
    sent = json.load(open(sent_path, 'r'))
    return received, sent
    
def create_tree_from_json(tree,json,is_received):
    if(is_received):
        for to_add,transactions in json.items():
            if to_add not in tree:
                tree[to_add] = []
            for transaction in transactions:
                from_add = transaction["from_address"]
                if from_add not in tree:
                    tree[to_add].append(from_add) #Note to myself
    else:
        for from_add,transactions in json.items():
            if from_add not in tree:
                tree[from_add] = []
            for transaction in transactions:
                to_add = transaction["to_address"]
                if to_add not in tree:
                    tree[from_add].append(to_add)
                    
def create_tree(tree,level_limit):
    for i in range(level_limit,0,-1):
        cur_json_received,cur_json_sent = read_parent_transactions(i)
        create_tree_from_json(tree,cur_json_received,True)
        create_tree_from_json(tree,cur_json_sent,False)
    cur_json_received,cur_json_sent = read_degree_transactions(0)
    create_tree_from_json(tree,cur_json_received,True)
    create_tree_from_json(tree,cur_json_sent,False)
    for i in range(1,level_limit + 1):
        cur_json_received,cur_json_sent = read_child_transactions(i)
        create_tree_from_json(tree,cur_json_received,True)
        create_tree_from_json(tree,cur_json_sent,False)
    return tree


def create_unique_node_name(name, level):
    return f"{name}_{level}"

def create_display_name(name,level):
    return f"{name[-4:]}_{level}"

def add_nodes(graph, tree, parent, visited_nodes, level=0, display_names={}, parent_map={}):
    if parent in visited_nodes:
        return
    visited_nodes.add(parent)
    unique_parent = create_unique_node_name(parent, level)
    if unique_parent not in graph:
        graph.add_node(unique_parent)
        display_names[unique_parent] = create_display_name(parent,level)
        if parent not in parent_map:
            parent_map[parent] = unique_parent 

    for child in tree.get(parent, []):
        if child is None:
            continue
        unique_child = create_unique_node_name(child, level + 1)
        if child not in parent_map:
            if unique_child not in graph:
                graph.add_node(unique_child)
                display_names[unique_child] = create_display_name(child,level + 1)
                parent_map[child] = unique_child
            add_nodes(graph, tree, child, visited_nodes, level + 1, display_names, parent_map)

def add_edges(graph, tree, parent, visited_edges, level=0, parent_map={}):
    if parent in visited_edges:
        return
    visited_edges.add(parent)
    unique_parent = parent_map[parent]
    parent_level = int(unique_parent[-1])
    for child in tree.get(parent, []):
        if child is None:
            continue
        unique_child = parent_map[child]
        child_level = int(unique_child[-1])
        if child_level > parent_level:
            graph.add_edge(unique_parent, unique_child)
            add_edges(graph, tree, child, visited_edges, level + 1, parent_map)
        else:
            for child_per in tree[parent]:
                name = create_unique_node_name(child_per, child_level)
                display_name = create_display_name(name,child_level)
                G.add_node(name)
                display_names[name] = display_name
                parent_name = parent_map[parent]
                G.add_edge(parent_name,name)

G = nx.Graph()
display_names = {}
parent_map = {}
tree = {}
visited_nodes = set()
visited_edges = set()
level_limit = 5
create_tree(tree,level_limit)

for parent in tree:
        if parent not in visited_nodes:
            add_nodes(G, tree, parent, visited_nodes, level=0, display_names=display_names, parent_map=parent_map)

for parent in tree:
        if parent not in visited_edges:
            add_edges(G, tree, parent, visited_edges,level=0, parent_map=parent_map)

net = Network(height="750px", width="100%", directed=False)

net.from_nx(G)

color_map = {
    0: "#ff6666",      # Red
    1: "#66b3ff",      # Blue
    2: "#66ff66",      # Green
    3: "#ffcc66",      # Orange
    4: "#c266ff",      # Purple
    5: "#66ffcc",       # Teal
    6: "#ff66cc",       # Pink
    7: "#ffff66",       # Yellow
    8: "#66ffff",       # Cyan
    9: "#cc9966",       # Brown
    10: "ff8c00"         # Dark Orange
}

for node in net.nodes:
    name = display_names[node["id"]]
    print(name)
    node["label"] = name
    node["title"] = name
    node["color"] = color_map[int(name[-1])]

net.show("transactions_tree_2.html",notebook=False)
