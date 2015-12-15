# -*- coding: utf-8 -*-
'''
OctoDog Web Application
Draw 3D scatter plot in rank page
#TODO-change url name 
http://projboard.sinaapp.com/
@author: bambooom
'''

import plotly.plotly as py
import plotly.graph_objs as go
from get_repos_stats import *

graph_data = fetch_list(fetch_stat())

def draw3d(graph_data):
	# repos_stats=[{name:AAA,commits:B,attention:C,uneven:D},{},...]

    trace = go.Scatter3d(
        x=graph_data[3],
        y=graph_data[1],
        z=graph_data[2],
        mode='markers+text',
        text=graph_data[0],
        textposition="topcenter",
        marker=dict(
            color='rgb(0, 255, 255)',
            size=5,
            symbol='circle'
            ),
            
        )

    data=[trace]
    layout = go.Layout(
        scene=go.Scene(
           aspectratio=dict(
                x=1,
                y=1,
                z=1
            ),
           xaxis=dict(
                title="uneven",
                type="linear",
                titlefont=dict(
                    color="rgb(31,119,180)"),
                tickfont=dict(
                    color="rgb(21,119,180)")
            ),
           yaxis=dict(
                title="commits",
                type="linear",
                titlefont=dict(
                    color="rgb(225,127,14)"),
                tickfont=dict(
                    color="rgb(225,127,14)")
            ),
           zaxis=dict(
                title="attention",
                type="linear",
                titlefont=dict(
                    color="rgb(44,160,44)"),
                tickfont=dict(
                    color="rgb(44,160,44)")
            )
        ),
        showlegend=False,
        autosize=True,
        height=419,
        width=1010

    )
    
    fig = go.Figure(data=data, layout=layout)
    plot_url=py.plot(fig, auto_open=False)
    return plot_url