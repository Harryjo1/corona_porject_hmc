
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output

from IPython import display
from ipywidgets import interact, widgets
from datetime import datetime



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_html_components as html

#url = 'https://github.com/Harryjo1/corona_porject_hmc/edit/master'

data_confirmed = pd.read_csv('time_series_2019-ncov-Confirmed.csv')
data_death = pd.read_csv('time_series_2019-ncov-Deaths.csv')
data_recovered = pd.read_csv('time_series_2019-ncov-Recovered.csv')

# data_confirmed = pd.read_csv(r'D:\Neoma\Finnce and big data\data vizualisation\time_series_2019-ncov-Confirmed.csv') 
# data_death = pd.read_csv(r'D:\Neoma\Finnce and big data\data vizualisation\time_series_2019-ncov-Deaths.csv') 
# data_recovered = pd.read_csv(r'D:\Neoma\Finnce and big data\data vizualisation\time_series_2019-ncov-Recovered.csv') 

data_confirmed = data_confirmed.drop(["Lat","Long","Province/State","Country/Region"],axis="columns")
data_death = data_death.drop(["Lat","Long","Province/State","Country/Region"],axis="columns")
data_recovered = data_recovered.drop(["Lat","Long","Province/State","Country/Region"],axis="columns")

print(data_recovered)

#data_confirmed["1/21/20 22:00"] = data_confirmed["1/21/20 22:00"].fillna(0)

data_confirmed = data_confirmed.fillna(0)
data_death = data_death.fillna(0)
data_recovered = data_recovered.fillna(0)



data_confirmed = data_confirmed.sum(axis = 0)
data_confirmed = data_confirmed.to_frame()

data_death = data_death.sum(axis = 0)
data_death = data_death.to_frame()


data_recovered = data_recovered.sum(axis = 0)
data_recovered = data_recovered.to_frame()



data_confirmed.reset_index(inplace = True) 
data_death.reset_index(inplace = True) 
data_recovered.reset_index(inplace = True) 



data_confirmed = data_confirmed.rename(columns={"index": "Dates", 0: "Confirmed"})
data_death = data_death.rename(columns={"index": "Dates", 0: "Deaths"})
data_recovered = data_recovered.rename(columns={"index": "Dates", 0: "Recoveries"})



DATA  = data_confirmed.merge(data_death).merge(data_recovered)



DATA["Confirmed"].iloc[-1]




fig = go.Figure()
fig.add_trace(go.Scatter(
                x=DATA.Dates,
                y=DATA['Confirmed'],
                name="Confirmed",
                line_color='deepskyblue',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=DATA.Dates,
                y=DATA['Deaths'],
                name="Deaths",
                line_color='red',
                opacity=0.8))

fig.add_trace(go.Scatter(
                x=DATA.Dates,
                y=DATA['Recoveries'],
                name="Recoveries",
                line_color='green',
                opacity=0.8))

# Use date string to set xaxis range
fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
fig.update_layout({"paper_bgcolor":"#404040","plot_bgcolor":"#404040","font":{'color':'white'}})
fig.update_layout(
    legend=dict(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(
            family="sans-serif",
            size=12,
            color="white"
        ),
        bordercolor="Black",
        borderwidth=0
    )
)

fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    )
)
#fig.show()




def graphique_Nb_enfant(annee):
    
    df =DATA[DATA.Dates == annee]
    
    
    date = df.iloc[0,0]                  
    print(date)

    x1 =df.iloc[0,1]
    x2 = df.iloc[0,2]
    x3 = df.iloc[0,3]

    fig = go.Figure(data=[
        go.Bar(name='confirmed', x=[date], y=[x1]),
        go.Bar(name='death', x=[date], y=[x2]),
        go.Bar(name='recovered', x=[date], y=[x3])
    ])
    # Change the bar mode
    fig.update_layout()
    fig.update_layout({'barmode':'stack',"paper_bgcolor":"#404040","plot_bgcolor":"#404040","font":{'color':'white'}})
    return fig




#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server =app.server


app.layout = html.Div([
    html.H2("Coronavirus"),
    html.Div([
#=============== 1 sous div================================        
         html.Div([
             html.Div([
                 html.P("Total confirmed"),
                 html.P(DATA["Confirmed"].iloc[-1],style={"color":"Tomato"})
                 ],style={"background":"#404040","width" : "150px"}),
             
             html.Div([
                 html.P("Total Death"),
                 html.P(DATA["Deaths"].iloc[-1],style={"color":"Tomato"})
                 ],style={"background":"#404040","width" : "150px"}),
             
             html.Div([                 
                 html.P("Total Recoveries"),
                 html.P(DATA["Recoveries"].iloc[-1],style={"color":"Tomato"})
                 ],style={"background":"#404040","width" : "150px"}),]),
#=============== fin 1 sous div================================          
               
        
        html.Div([
            html.P("Propagation virus"),
            html.P(DATA["Confirmed"].iloc[-1])
        ],style={"background":"#404040","width" : "750px"}),
        
        
        html.Div([dcc.Graph(id="evolution-cas",figure=fig),
                  html.Div([html.Span("Choix date  : "),
                           dcc.Dropdown(
                            id='choix-date',
                            options=[ {'label' : d, 'value':d} for d in DATA["Dates"]],
                            value="1/27/20 20:30",
                            style={"background": "rgba(0,0,0,1)","color":"black"})
                          ]),
                  
                  dcc.Graph(id="cas-par-date",figure=graphique_Nb_enfant("1/27/20 20:30"))
                  ],style={"background":"#404040","width" : "500px"})
        
        
        ],style={"display" : "flex","justify-content":"space-between"})
],style={"background":"#000","color":"white"})

@app.callback(
    Output(component_id='cas-par-date', component_property='figure'),
    [Input(component_id='choix-date', component_property='value')]
)
def update_graph(date):
    return graphique_Nb_enfant(date)

app.run_server(debug = True)
