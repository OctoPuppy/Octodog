# -*- coding: utf-8 -*-
'''
OctoDog Web Application
Draw 3D scatter plot in rank page
http://octodog.sinaapp.com/
@author: bambooom
'''

import plotly.plotly as py
import plotly.graph_objs as go
#from get_repos_stats import *

#graph_data = fetch_list(fetch_stat())

#graph_data = [['mipe', 'straypetshelper', 'RIA-Brain-truster', 'PhotoxOrganizer', 'imoodmapGroup', 'Hunting-for-Great-Books', 'jizhemai', 'whenmgone', 'less-habit', 'Octodog', 'Stock_Pickup_and_Reminding', 'iMatch', 'housebuy', 'RUNMAP'], [1, 111, 2, 15, 45, 75, 16, 4, 3, 77, 29, 28, 7, 27], [4, 11, 0, 3, 8, 0, 5, 4, 2, 20, 13, 8, 1, 17], [0.0, 0.59, 0.0, 0.0, 1.92, 0.0, 0.0, 0.0, 0.0, 0, 2.16, 1.44, 0.0, 0.0]]



def draw3d(graph_data):
    py.sign_in("bambooom", "k01s1p8rme")

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

if __name__ == '__main__':
    plot = draw3d(graph_data)
    print plot
