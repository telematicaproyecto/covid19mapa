from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
from decimal import Decimal 

app = Flask(__name__)
db_path = 'labasededatos/BDmedallo.db'
mapa = dash.Dash(__name__,server=app,routes_pathname_prefix='/mapa/')
df = pd.read_excel('BasedeDatosCovidMaps.xls')
cnx = sqlite3.connect(db_path)
database = pd.read_sql_query("SELECT * FROM covidpositivo", cnx)
data = pd.concat([database,df],axis=0)
vectorLat = data['latitud']
vectorLon = data['longitud']
cnx.commit()
cnx.close()


@app.route('/usuario', methods=["POST", "GET"])
def home():
   if request.method=="POST":
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellidos")
        correo = request.form.get("correo")
        edad = request.form.get("edad")
        sexo = request.form.get("sexo")
        corona = request.form.get("corona")
        latitud = request.form.get("latitud")
        longitud = request.form.get("longitud")
        if corona == "SI":
            con = sqlite3.connect(db_path)
            cur = con.cursor()
            cur.execute("INSERT INTO covidpositivo VALUES(" +latitud + "," + longitud+ ")")
            con.commit()
            con.close()
        return redirect('/mapa') 

@app.route('/mapa')
def graficar():
    df = pd.read_excel('BasedeDatosCovidMaps.xls')
    cnx = sqlite3.connect(db_path)
    database = pd.read_sql_query("SELECT * FROM covidpositivo", cnx)
    cnx.commit()
    cnx.close()
    data = pd.concat([database,df],axis=0)
    vectorLat = data['latitud']
    vectorLon = data['longitud']
    mapa.layout = html.Div([
            html.H1('Contagios En El Area Metropolitana De Medellin'),
        html.Button('Analizar Datos', id='submit-val', n_clicks=0),
        html.H1(id='test'),
            html.Div(id='text-content'),
           dcc.Graph(id='map', figure={
                'data': [{
                'lat': vectorLat,
                        'lon': vectorLon,
                'marker': {
                            'color': 'red',
                            'size': 20,
                            'opacity': 0.6
                        },
                        'customdata': 2,
                        'type': 'scattermapbox'
                   }],
                'layout': {
                        'mapbox': {
                            'accesstoken': 'pk.eyJ1IjoibGVvbmFyZG9iZXRhbmN1ciIsImEiOiJjazlybGNiZWcwYjZ6M2dwNGY4MmY2eGpwIn0.EJjpR4klZpOHSfdm7Tsfkw',
                    'center' :{
                        'lat' : 6.242095,
                        'lon' : -75.589626
                    },
                    'zoom' : 10,
                    'style' : 'dark'
                        },
                        'hovermode': 'closest',
                        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
                }
            })
    ])
@mapa.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('submit-val', 'n_clicks')])

@app.route('/', methods =["GET"])
def logueo():
    """con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS data")
    cur.execute("CREATE TABLE covidpositivo (latitud DOUBLE, longitud DOUBLE)")
    con.commit()
    con.close()"""
    data = pd.concat([database,df],axis=0)
    vectorLat = data['latitud']
    vectorLon = data['longitud']
    return render_template("index.html")


if __name__ == '__main__':
    graficar()
    mapa.run_server(debug = True, host = '0.0.0.0', port = 80)
