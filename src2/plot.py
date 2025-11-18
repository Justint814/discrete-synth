import plotly.graph_objects as go
import numpy as np


def simple_plot(array, name, type="markers"):
    x_vals = np.arange(0, len(array), 1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=array, mode=type, name=name)) 

    fig.update_traces(line=dict(width=.6)) #Update line width
    fig.update_traces(marker=dict(size=2)) #Update marker size

    fig.update_layout(
        title=name,
        xaxis_title="tick",
        yaxis_title="Amplitude"
    ) #Add titles

    fig.show()  # Show the figure. 

ADSR_arr = np.load("/Users/justintraywick/Coding/discrete-synth/discrete-synth/data/ADSR_arr.npy", allow_pickle=True)

simple_plot(ADSR_arr, 'name', type="lines")

