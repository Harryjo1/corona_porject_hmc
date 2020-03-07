import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output

from IPython import display
from ipywidgets import interact, widgets
from datetime import datetime



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go



data_confirmed = pd.read_csv('https://raw.githubusercontent.com/Harryjo1/corona_porject_hmc/master/time_series_2019-ncov-Confirmed.csv') 
data_death = pd.read_csv("https://raw.githubusercontent.com/Harryjo1/corona_porject_hmc/master/time_series_2019-ncov-Deaths.csv") 
data_recovered = pd.read_csv("https://raw.githubusercontent.com/Harryjo1/corona_porject_hmc/master/time_series_2019-ncov-Recovered.csv") 

data_confirmed = data_confirmed.drop(["Lat","Long","Province/State","Country/Region"],axis="columns")
data_death = data_death.drop(["Lat","Long","Province/State","Country/Region"],axis="columns")
data_recovered = data_recovered.drop(["Lat","Long","Province/State","Country/Region"],axis="columns")

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

#graphique_Nb_enfant("1/21/20 22:00")



def map (var,date,chine) :
    map_confirmed = pd.read_csv('https://raw.githubusercontent.com/Harryjo1/corona_porject_hmc/master/map-Confirmed.csv') 
    map_death = pd.read_csv('https://raw.githubusercontent.com/Harryjo1/corona_porject_hmc/master/map-Deaths.csv') 
    map_recovered = pd.read_csv('https://raw.githubusercontent.com/Harryjo1/corona_porject_hmc/master/map-Recovered.csv')
    token="pk.eyJ1IjoibW91bmlyZXR0YW91dGkiLCJhIjoiY2s3Z2J3cXFlMDNqNDNrbzNmbzA0aXB1NiJ9.fK1-uJet5AIzWloTmssKGw" 
    
    #  definition des echelles de couleurs : rouge pour les morts, jaune - orange pour les confirmés, verts pour les guerris
    scales_dead = [[0, "rgb(225,153,153)"],
                [0.25, "rgb(225,130,130)"],
                [0.45, "rgb(225,110,110)"],
                [0.65, "rgb(225,70,70)"],
                [0.85, "rgb(251,20,20)"],
                [1, "rgb(227,0,0)"]]
    scales_confirmed = [[0, "rgb(255,255,102)"],
                [0.25, "rgb(255,255,51)"],
                [0.45, "rgb(255,255,0)"],
                [0.65, "rgb(255,153,51)"],
                [0.85, "rgb(255,158,0)"],
                [1, "rgb(255,158,0)"]]
    scales_recorvery = [[0, "rgb(153,255,153)"],
                [0.25, "rgb(102,255,102)"],
                [0.45, "rgb(51,255,51)"],
                [0.65, "rgb(0,255,0)"],
                [0.85, "rgb(0,255,0)"],
                [1, "rgb(0,204,0)"]]
    
    
#   condition sur la variable à selectionner  : Map des cas confirmé, des guerris, ou des morts par date 
    
    if var == "confirmed" : 
        df = map_confirmed
        scale = scales_confirmed
        Title ="Nb confirmed cases"
    elif var == "recovered" : 
        df = map_recovered
        scale = scales_recorvery
        Title = "Nb recovered cases"
    elif var == "death" : 
        df = map_death
        scale = scales_dead
        Title="Nb dead cases"
    
#     carte avec ou sans affichage de la chine : 1 sans chine , 0 avec chine 
    
    if chine == 1 :
        Lat = "Lat2"
        Long = "Long2"
        sizemax = 500
    elif chine == 0 : 
        Lat = "Lat"
        Long = "Long"
        sizemax = 100
    
    fig=px.scatter_mapbox(df, lat=Lat, lon=Long, hover_name="Country/Region", color=df[date], size=df[date], size_max = sizemax,
                          hover_data=["Province/State", date],
                          color_continuous_scale=scale ,
                          zoom=3, 
                          height=500
                         )
    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(coloraxis_colorbar=dict(title=Title,))
    fig.update_layout(mapbox=dict(
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=28,
            lon=107
        ),
        pitch=0
    ))
    
    
    return fig



external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
#server =app.server


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
            html.Div([html.Span("Choix map  : "),
                       dcc.Dropdown(
                        id='choix-map',
                        options=[ {'label' : 'Cas soignés', 'value':"recovered"},
                                  {'label' : 'Cas confirmés', 'value':"confirmed"},
                                  {'label' : 'Cas morts', 'value':"death"}],
                        value="recovered",
                        style={"background": "rgba(0,0,0,1)","color":"black"}),
                      dcc.Graph(id="map-cas",figure=map("recovered",'2/14/2020 11:23',1))
                     ])
        ],style={"background":"#404040","width" : "800px","height":"580px"}),
        
        
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
],style={"background":"#000","color":"white","padding":"10px"})

@app.callback(
    Output(component_id='cas-par-date', component_property='figure'),
    [Input(component_id='choix-date', component_property='value')]
)
def update_graph(date):
    return graphique_Nb_enfant(date)


@app.callback(
    Output(component_id='map-cas', component_property='figure'),
    [Input(component_id='choix-map', component_property='value')]
)
def update_graph(type):
    return map(type,'2/14/2020 11:23',1)

app.run_server()

