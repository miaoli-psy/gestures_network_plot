# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 12:21:56 2024

@author: Miao
"""

import os
import networkx as nx
import plotly.graph_objects as go
import random
import plotly.io as pio


import dash
from dash import dcc, html

# open the plot in browser
pio.renderers.default = 'browser'

# path
gestuers_folder = "./gesture_photos"


# get list of the images
images_list = [f for f in os.listdir(gestuers_folder) if os.path.isfile(os.path.join(gestuers_folder, f))]


# relations
relationships = [
    ("G1_spray.png", "G7_medWrap.png"), 
    ("G2_poke.png", "G3_gachette.png"),
    ("G6_preciDisk.png", "G7_medWrap.png"),
    ("G6_preciDisk.png", "G11_thumb2f.png"),
    ("G7_medWrap.png", "G9_thumb3f.png"),
    ("G8_LateralPinch.png", "G11_thumb2f.png"),
    ("G9_thumb3f.png", "G7_medWrap.png"),
    ("G9_thumb3f.png", "G8_LateralPinch.png"),
    ("G10_extenType.png", "G4_palm.png"),
    ("G10_extenType.png", "G7_medWrap.png"),
    ("G11_thumb2f.png", "G6_preciDisk.png"),
    ("G11_thumb2f.png", "G7_medWrap.png"),
    ("G11_thumb2f.png", "G9_thumb3f.png"),
    ("G12powerSphere.png", "G7_medWrap.png"),
    ("G12powerSphere.png", "G1_spray.png"),
    ("G12powerSphere.png", "G4_palm.png")]


# the graph
G = nx.Graph()
G.add_edges_from(relationships)

# posi of the nodes; increase k for better spacing if needed
pos = nx.spring_layout(G, k=1, seed= 3)  # 

# extract the node positions, names, and edge positions
edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)  # to break the line between edges
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

# Draw the edges
edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#888'), 
    hoverinfo='none',
    mode='lines')

# draw  nodes here
node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

# random color for each node
node_colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in G.nodes()]

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',  # show both markers and labels
    hoverinfo='text',
    text=[node for node in G.nodes()],  # node labels
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=50,  # node size
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        color=node_colors
    ),
    textposition="bottom center"  #position labels below the nodes
)

# layout for Plotly
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    title='Gestures connections',
                    titlefont_size=20,  
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=40, l=40, r=40, t=40),  #  margins
                    annotations=[dict(
                        text="Click a node to see its connections.",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002
                    )],
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False),
                    width=1000,  # figure width
                    height=800  # figure height
                ))

# Show the figure in the default web browser
fig.show()

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Network Graph"),
    dcc.Graph(figure=fig)  # The Plotly graph
])

# Required for PythonAnywhere
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)