import io
import datetime
import random as rand
import json
import os
import base64
import datetime
import pandas as pd
import dash
import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ALL, MATCH
import dash_html_components as html
import dash_table as dt
import pprint

def layout(app):
    return html.Div(children = [
            dt.DataTable(),
            html.Div(id = 'struct', className = 'app-div', children = [
                html.Hr(style = {'width': '500px'}),
                 html.P('Choose dimension of file...', style = {'color':'#fec036'}),
                 dcc.RadioItems(
                     id = 'dimenzion', options = [{'label': i, 'value': i} for i in ['2D', '3D']],
                             value = 'none',
                             labelStyle={'display': 'inline-block'},
                             style={'textAlign': 'center','margin': '15px', 'color':'#ffffff'},
                         ),
                 html.Hr(style = {'width': '500px'}),
                 html.P('Choose metrick which would be use...', style = {'color':'#fec036'}),
                 dcc.RadioItems(
                     id = 'metrick', options = [{'label': i, 'value': i} for i in ['Euclides', 'Manhaton', 'Minkovski']],
                             value='Euclides',
                             labelStyle={'display': 'inline-block'},
                             style={'textAlign': 'center','margin': '15px', 'color':'#ffffff'},
                         ),
                 html.Hr(style = {'width': '500px'}),
                 html.P('How many clusters, do you want to use...', style = {'color':'#fec036'}),
                 dcc.Slider(
                     id = 'numer_clust',
                     min=1,
                     max=10,
                     marks={i: '{}'.format(i) for i in range(11)},
                     value=5,
                     ),  
                 html.Hr(style = {'width': '500px'}),
                 html.Div(className='app-controls-block', children=[
                     html.Div(className='app-controls-name', children='Centroid pozicion', style = {'color':'#fec036'}),
                     dcc.Dropdown(
                         id='centr-poz',
                         options=[
                             {'label': 'Random generated pozition.', 'value': 'rand'},
                             {'label': 'Enterd myself pozition', 'value': 'enter'}
                         ],
                         value='rand'
                     ),
                 ]),
                 html.Div(id = 'coordinates-3d', className = 'centroid-own', children = [     
                     html.Hr(style = {'width': '500px'}),
                    dt.DataTable(
                        id='adding-rows-table-3d',
                        columns=[{
                            'name': 'x{}'.format(i),
                            'id': 'x{}'.format(i),
                            'deletable': True,
                            'renamable': True
                        } for i in range(2)],
                        data=[],
                        editable=True,
                        row_deletable=True
                    ),
                 ]),
                 html.Div(id='output-container-button', children = [
                     html.Div(id = 'container', children = [
                     html.Hr(style = {'width': '500px'}),
                     dcc.Upload(
                         id='upload-data',
                         children=html.Div([
                             'Drag and Drop or ',
                             html.A('Select Files')
                         ]),
                         style={'width': '500px', 'height': '60px', 'lineHeight': '60px', 'borderWidth': '1px', 
                                'borderStyle': 'dashed','borderRadius': '5px','textAlign': 'center','margin': '15px', 'color':'#fec036'},
                         multiple=True
                         )
                     ]),
                     html.Div(id='output-data-upload', style = {'display': 'none'}),
                     html.Hr(style = {'width': '500px'}),
                     html.Div(className='metods-contr', children='Which metod you want?', style = {'color':'#fec036'}),
                         dcc.Dropdown(
                             id='metod-dis',
                             options=[
                                 {'label': 'K-means.', 'value': 'means'},
                                 {'label': 'K-medoids', 'value': 'medoids'}
                             ],
                             value='means'
                         ),
                     html.Hr(style = {'width': '500px'}),
                     html.Div(className='app-start-block', children=[
                         html.Div(className='app-start-name', children='What do you prefer?', style = {'color':'#fec036'}),
                         dcc.Dropdown(
                             id='step-step',
                             options=[
                                 {'label': 'Result', 'value': 'res'},
                                 {'label': 'Step by Step', 'value': 'step'}
                             ],
                             value='res'
                         ),
                     ]),
                     html.Div(id = 'res',className='app-res-but', children=[
                         html.Hr(style = {'width': '500px'}),
                         html.A(
                             html.Button(
                                 id='complete-but',
                                 className='control-complete',
                                 children="Next",
                                 n_clicks=0,
                                 style = {'color':'#fec036'}
                             ),
                         ),
                         html.A(
                             html.Button(
                                 id='print-but',
                                 className='control-print',
                                 children="Print centroid",
                                 n_clicks=0,
                                 style = {'color':'#fec036'}
                             ),
                         ),
                         html.Hr(style = {'width': '500px'}),
                     ]),
                 ]),
            ], style={'width': '30%', 'display': 'inline-block', 'borderRadius': '20px',
                       'textAlign': 'center', "background-color": "#303030"}),
            html.Div(id = 'graph', className="six columns", children=[
                        ], style={'width': '66%', 'float': 'right', 'display': 'inline-block'},
                    ),
            html.Div(id = 'centroid', children = [
                ], style = {'display': 'none'}),

            html.Div(id = 'some', children = [
                ], style = {'display': 'none'})
        ])

def callbacks(app):
    @app.callback(
            Output('container', 'style'),
            [Input('dimenzion', 'value')],
            )

    def show_hide_uploaded(center):
        if center == '2D' or center == '3D':
            return {'display': 'inline-block'}
        else:
            return {'display': 'none'}

    @app.callback(
            Output('print-but', 'style'),
            [Input('step-step', 'value')],
            )

    def show_hide_uploaded(center):
        if center == 'step':
            return {'display': 'inline-block'}
        else:
            return {'display': 'none'}

    @app.callback(
            Output('coordinates-3d', 'style'),
            [Input('centr-poz', 'value')],
        )
    def show_hide_uploaded(center):
        if center == 'enter':
            return {'display': 'inline-block'}
        else:
            return {'display': 'none'}

    @app.callback(
        Output('adding-rows-table-3d', 'columns'),
        [Input('centr-poz', 'value'),
         Input('dimenzion', 'value')],
        [State('adding-rows-table-3d', 'columns')])

    def update_columns(poz, dimenz, columns):
        if dimenz == '3D' and len(columns) < 3:
            columns.append({
                'id': 'x2', 'name': 'x2',
                'renamable': True, 'deletable': True
            })
        elif dimenz == '2D' and len(columns) > 2:
            columns.pop(2)
        return columns

    @app.callback(
        Output('adding-rows-table-3d', 'data'),
        [Input('numer_clust', 'value')],
        [State('adding-rows-table-3d', 'data'),
         State('adding-rows-table-3d', 'columns')])

    def add_row(n_clicks, rows, columns):
        rows.clear()
        for i in range(n_clicks):
            if len(rows) < n_clicks:
                rows.append({c['id']: '' for c in columns})
        return rows
        
    def parse_contents(contents, filename, _):
        _, content_string = contents.split(',')

        decoded = base64.b64decode(content_string).decode('UTF-8')
        answer = None
        try:
            if filename.endswith('.csv'):
                # Assume that the user uploaded a CSV file
                df = pd.read_csv(io.StringIO(decoded))
                df = df.to_dict(orient='records')
                answer = df
            elif filename.endswitch('.txt'):
                df = pd.read_fwf(io.StringIO(decoded))
                df = df.to_dict(orient='records')
                answer = df
        except Exception as e:
            answer = html.Div(['There was an error processing this file.'])
        return answer

    @app.callback(Output('output-data-upload', 'children'),
                  [Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified'),
                   State("output-data-upload", "children")])

    def update_output(list_of_contents, list_of_names, list_of_dates, data):
        answer = None
        if data is None:
            array = []
        else:
            array = json.loads(data)
        if list_of_contents is not None:
            children = list((parse_contents(c, n, d)
                    for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
                )
            )
            children = children[0]
            array = children
            answer = json.dumps(array)
        return answer

    @app.callback(Output('some', 'children'),
                  [Input('print-but', 'n_clicks')],
                  [State('dimenzion', 'value'),
                   State('metrick', 'value'),
                   State('step-step', 'value'),
                   State('numer_clust', 'value'),
                   State('centr-poz', 'value'),
                   State('adding-rows-table-3d', 'data'),
                   State('metod-dis', 'value'),
                   State('centroid', 'children'),
                   State('upload-data', 'filename')
                   ])
    def print(print, dimension, metrick, step, number_clust, pozition, centr_row, metod, centroid, filename):
        if centroid is None:
            return None
        elif centroid is not None:
            array = json.loads(centroid)
            centroid_last = read_data(array, dimension)
            poradi = new_txt()
            text_out_headline(filename, dimension, number_clust, poradi)
            for i in range(len(centroid_last[0])):
                if dimension == '2D':
                    text_out_2d(centroid_last[0][i], centroid_last[1][i], poradi)
                elif dimension == '3D':
                    text_out_3d(centroid_last[0][i], centroid_last[1][i], centroid_last[2][i], poradi)
            text_out_finish("It's on you", poradi)
            return None

    @app.callback([Output('graph', 'children'),
                   Output('centroid', 'children')],
                  [Input('complete-but', 'n_clicks'),
                   Input('output-data-upload', 'children')],
                  [State('dimenzion', 'value'),
                   State('metrick', 'value'),
                   State('step-step', 'value'),
                   State('numer_clust', 'value'),
                   State('centr-poz', 'value'),
                   State('adding-rows-table-3d', 'data'),
                   State('metod-dis', 'value'),
                   State('centroid', 'children'),
                   State('upload-data', 'filename')
                   ])

    def display_graf(button_st, data, dimension, metrick, step, number_clust, pozition, centr_row, metod, centroid, filename):
        points = []
        if dimension == '2D':
            array = json.loads(data)
            x1 = []
            y1 = []
            for i in range(len(array)): 
                x1.append(float(array[i]["x1"]))
                y1.append(float(array[i]["x2"]))
            points.append(x1)
            max_x = max(x1)
            min_x = min(x1)
            points.append(y1)
            max_y = max(y1)
            min_y = min(y1)
        elif dimension == '3D':
            array = json.loads(data)
            x1 = []
            y1 = []
            z1 = []
            for i in range(len(array)): 
                x1.append(float(array[i]["x1"]))
                y1.append(float(array[i]["x2"]))
                z1.append(float(array[i]["x3"]))
            points.append(x1)
            max_x = max(x1)
            min_x = min(x1)
            points.append(y1)
            max_y = max(y1)
            min_y = min(y1)
            points.append(z1)
            max_z = max(z1)
            min_z = min(z1)
        if dimension == '2D' and button_st == 0:
            fig = go.Figure(data = [go.Scatter(x = x1, y = y1, mode='markers')])
            return [dcc.Graph(id="graph-3d-plot", figure = fig,
                                      style={"height": "95vh", 'width':'130vh', 'margin-top':'20px', 'margin-right': '20px'}), None]
        elif dimension == '3D' and button_st == 0:
            fig = go.Figure(data = [go.Scatter3d(x = x1, y = y1, z = z1, mode='markers')])
            return [dcc.Graph(id="graph-3d-plot", figure = fig,
                                      style={"height": "95vh", 'width':'130vh', 'margin-top':'20px', 'margin-right': '20px'}), None]
        index = []
        sorted = []
        centroid_start = []
        if dimension == '2D':
            if pozition == 'rand':
                centroid_start = rand_coordin_2d(number_clust, max_x, max_y, min_x, min_y)
                if metod == 'medoids':
                    centroid_start = medoids_centroid(points, centroid_start)
            elif pozition == 'enter':
                centroid_start = read_centroid(centr_row, '2D')
                if metod == 'medoids':
                    centroid_start = medoids_centroid(points, centroid_start)
        elif dimension == '3D':
            if pozition == 'rand':
                centroid_start = rand_coordin_3d(number_clust, max_x, max_y, max_z, min_x, min_y, min_z)
                if metod == 'medoids':
                    centroid_start = medoids_centroid(points, centroid_start)
            elif pozition == 'enter':
                centroid_start = read_centroid(centr_row, '3D')
                if metod == 'medoids':
                    centroid_start = medoids_centroid(points, centroid_start)

        if step == 'res' and button_st != 0:
            poradi = new_txt()
            text_out_headline(filename, dimension, number_clust, poradi)
            j = 0
            centroid_last = centroid_start
            centroid_last_1 = []
            memory = 0
            while True:
                figu = make_subplots(rows=1, cols=1)
                if dimension == '2D':
                    figu = make_subplots(rows=1, cols=1, specs=[[{'type': 'xy'}]])
                    index = sort_data_to_cluster(points, centroid_last, metrick, '2D')
                    sorted = sort_data(points, index, centroid_last, '2D')
                    for i in range(len(sorted)):
                        figu.add_trace(go.Scatter(x = sorted[i][0], y = sorted[i][1], mode='markers', name='Cluster ' + str(i + 1) + ' group'), row=1, col=1)
                    figu.add_trace(go.Scatter(x = centroid_last[0], y = centroid_last[1], mode='markers', marker=dict(size=20, color=0), name='Clusters'), row=1, col=1)
                elif dimension == '3D':
                    figu = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter3d'}]])
                    index = sort_data_to_cluster(points, centroid_last, metrick, '3D')
                    sorted = sort_data(points, index, centroid_last, '3D')
                    for i in range(len(sorted)):
                        figu.add_trace(go.Scatter3d(x = sorted[i][0], y = sorted[i][1], z = sorted[i][2], mode='markers', name='Cluster ' + str(i + 1) + ' group'), row=1, col=1)
                    figu.add_trace(go.Scatter3d(x = centroid_last[0], y = centroid_last[1], z = centroid_last[2], mode='markers', marker=dict(size=20, color=0), name='Clusters'), row=1, col=1)
                centroid_last_1 = centroid_last
                difference = 0
                centroid_last = center_cluster(sorted, centroid_last)
                if metod == 'medoids':
                        centroid_last = medoids_centroid(points, centroid_last)
                for i in range(len(centroid_last)):
                    for j in range(len(centroid_last[0])):
                        difference += abs(centroid_last_1[i][j] - centroid_last[i][j])
                if abs(difference - memory) < 0.0001:
                    break
                memory = difference
                j += 1
            for i in range(len(centroid_last[0])):
                if dimension == '2D':
                    text_out_2d(centroid_last[0][i], centroid_last[1][i], poradi)
                elif dimension == '3D':
                    text_out_3d(centroid_last[0][i], centroid_last[1][i], centroid_last[2][i], poradi)
            text_out_finish(j, poradi)
            return [dcc.Graph(id="graph-3d-plot", figure = figu, style={"height": "95vh", 'width':'130vh', 'margin-top':'20px', 'margin-right': '20px'}), None]

        elif step == 'step' and button_st != 0:
            if centroid is None:
                centroid_last = centroid_start
            elif centroid is not None:
                array = json.loads(centroid)
                centroid_last = read_data(array, dimension)
            figu = make_subplots(rows=1, cols=1)
            if dimension == '2D':
                figu = make_subplots(rows=1, cols=1, specs=[[{'type': 'xy'}]])
                index = sort_data_to_cluster(points, centroid_last, metrick, '2D')
                sorted = sort_data(points, index, centroid_last, '2D')
                for i in range(len(sorted)):
                    figu.add_trace(go.Scatter(x = sorted[i][0], y = sorted[i][1], mode='markers', name='Cluster ' + str(i + 1) + ' group'), row=1, col=1)
                figu.add_trace(go.Scatter(x = centroid_last[0], y = centroid_last[1], mode='markers', marker=dict(size=20, color=0), name='Clusters'), row=1, col=1)
            elif dimension == '3D':
                figu = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter3d'}]])
                index = sort_data_to_cluster(points, centroid_last, metrick, '3D')
                sorted = sort_data(points, index, centroid_last, '3D')
                for i in range(len(sorted)):
                    figu.add_trace(go.Scatter3d(x = sorted[i][0], y = sorted[i][1], z = sorted[i][2], mode='markers', name='Cluster ' + str(i + 1) + ' group'), row=1, col=1)
                figu.add_trace(go.Scatter3d(x = centroid_last[0], y = centroid_last[1], z = centroid_last[2], mode='markers', marker=dict(size=20, color=0), name='Clusters'), row=1, col=1)
            centroid_last = center_cluster(sorted, centroid_last)
            if metod == 'medoids':
                    centroid_last = medoids_centroid(points, centroid_last)
            df = make_list_dict(centroid_last, dimension, number_clust)
            return [dcc.Graph(id="graph-3d-plot", figure = figu, style={"height": "95vh", 'width':'130vh', 'margin-top':'20px', 'margin-right': '20px'}), df]


def center_cluster(sorted, clusters):
    new_clusters = []
    if len(clusters) == 2:
        x = []
        y = []
        for j in range(len(clusters[0])):
            sum_x = 0
            sum_y = 0
            for k in range(len(sorted[j][0])):
                sum_x += sorted[j][0][k] - clusters[0][j]
                sum_y += sorted[j][1][k] - clusters[1][j]
            if len(sorted[j][0]) > 0:
                sum_x /= len(sorted[j][0])
                sum_y /= len(sorted[j][1])
                x.append(clusters[0][j] + sum_x)
                y.append(clusters[1][j] + sum_y)
            else:
                x.append(clusters[0][j])
                y.append(clusters[1][j])
        new_clusters.append(x)
        new_clusters.append(y)
    elif len(clusters) == 3:
        x = []
        y = []
        z = []
        for j in range(len(clusters[0])):
            sum_x = 0
            sum_y = 0
            sum_z = 0
            for k in range(len(sorted[j][0])):
                sum_x += sorted[j][0][k] - clusters[0][j]
                sum_y += sorted[j][1][k] - clusters[1][j]
                sum_z += sorted[j][2][k] - clusters[2][j]
            if len(sorted[j][0]) > 0:
                sum_x /= len(sorted[j][0])
                sum_y /= len(sorted[j][1])
                sum_z /= len(sorted[j][2])
                x.append(clusters[0][j] + sum_x)
                y.append(clusters[1][j] + sum_y)
                z.append(clusters[2][j] + sum_z)
            else:
                x.append(clusters[0][j])
                y.append(clusters[1][j])
                z.append(clusters[2][j])
        new_clusters.append(x)
        new_clusters.append(y)
        new_clusters.append(z)
    return new_clusters
        
def sort_data(data, sort, centroid, dim):
    sorted = []
    if dim == '3D':
        for i in range(len(centroid[0])):
            group = []
            x = []
            y = []
            z = []
            for j in range(len(sort)):
                if sort[j] == i:
                    x.append(data[0][j])
                    y.append(data[1][j])
                    z.append(data[2][j])
            group.append(x)
            group.append(y)
            group.append(z)
            sorted.append(group)
        return sorted
    elif dim == '2D':
        for i in range(len(centroid[0])):
            group = []
            x = []
            y = []
            for j in range(len(sort)):
                if sort[j] == i:
                    x.append(data[0][j])
                    y.append(data[1][j])
            group.append(x)
            group.append(y)
            sorted.append(group)
        return sorted

def sort_data_to_cluster(data, centroid, metrick, dimen):
    if dimen == '2D':
        sort = []
        for i in range(len(data[0])):
            distance = []
            for j in range(len(centroid[0])):
                if metrick == 'Euclides':
                    distance.append(((data[0][i] - centroid[0][j])**2 + (data[1][i] - centroid[1][j])**2)**(1/2.0))
                elif metrick == 'Manhaton':
                    distance.append(abs(data[0][i] - centroid[0][j]) + abs(data[1][i] - centroid[1][j]))
                elif metrick == 'Minkovski':
                    distance.append((abs(data[0][i] - centroid[0][j])**(1/2.0) + abs(data[1][i] - centroid[1][j])**(1/2.0))**2)
            sort.append(distance.index(min(distance)))
        return sort

    elif dimen == '3D':
        sort = []
        for i in range(len(data[0])):
            distance = []
            for j in range(len(centroid[0])):
                if metrick == 'Euclides':
                    distance.append(((data[0][i] - centroid[0][j])**2 + (data[1][i] - centroid[1][j])**2 + (data[2][i] - centroid[2][j])**2)**(1/2.0))
                elif metrick == 'Manhaton':
                    distance.append(abs(data[0][i] - centroid[0][j]) + abs(data[1][i] - centroid[1][j]) + abs(data[2][i] - centroid[2][j]))
                elif metrick == 'Minkovski':
                    distance.append((abs(data[0][i] - centroid[0][j])**(1/2.0) + abs(data[1][i] - centroid[1][j])**(1/2.0) + abs(data[2][i] - centroid[2][j])**(1/2.0))**2)
            sort.append(distance.index(min(distance)))
        return sort

def medoids_centroid(data, centroid):
    if len(centroid) == 2:
        centroid_start = []
        x = []
        y = []
        for i in range(len(centroid[0])):
            min = None
            index = None
            for j in range(len(data[0])):
                dist = ((data[0][j] - centroid[0][i])**2 + (data[1][j] - centroid[1][i])**2)**(1/2.0)
                if min == None:
                    index = j
                    min = dist
                elif dist < min:
                    index = j
                    min = dist
            x.append(data[0][index])
            y.append(data[1][index])
        centroid_start.append(x)
        centroid_start.append(y)
        return centroid_start

    elif len(centroid) == 3:
        centroid_start = []
        x = []
        y = []
        z = []
        for i in range(len(centroid[0])):
            min = None
            index = None
            for j in range(len(data[0])):
                dist = ((data[0][j] - centroid[0][i])**2 + (data[1][j] - centroid[1][i])**2 + (data[2][j] - centroid[2][i])**2)**(1/2.0)
                if min == None:
                    index = j
                    min = dist
                elif dist < min:
                    index = j
                    min = dist
            x.append(data[0][index])
            y.append(data[1][index])
            z.append(data[2][index])
        centroid_start.append(x)
        centroid_start.append(y)
        centroid_start.append(z)
        return centroid_start

def rand_coordin_2d(number_clust, max_x, max_y, min_x, min_y):
    cent_coordin = []
    x1 =[]
    y1 = []
    for i in range(number_clust):
        x = (min_x + (max_x - min_x)) * rand.random()
        x1.append(x)
        y = (min_y + (max_y - min_y)) * rand.random()
        y1.append(y)
    cent_coordin.append(x1)
    cent_coordin.append(y1)
    return cent_coordin

def rand_coordin_3d(number_clust, max_x, max_y, max_z, min_x, min_y, min_z):
    cent_coordin = []
    x1 =[]
    y1 = []
    z1 = []
    for i in range(number_clust):
        x = (min_x + (max_x - min_x)) * rand.random()
        x1.append(x)
        y = (min_y + (max_y - min_y)) * rand.random()
        y1.append(y)
        z = (min_z + (max_z - min_z)) * rand.random()
        z1.append(z)
    cent_coordin.append(x1)
    cent_coordin.append(y1)
    cent_coordin.append(z1)
    return cent_coordin

def read_centroid(data, dim):
    list = []
    x = []
    y = []
    if dim == '2D':
        for i in data:
            x.append(float(i['x0']))
            y.append(float(i['x1']))
        list.append(x)
        list.append(y)
    elif dim == '3D':
        z = []
        for i in data:
            x.append(float(i['x0']))
            y.append(float(i['x1']))
            z.append(float(i['x2']))
        list.append(x)
        list.append(y)
        list.append(z)
    return list

def make_list_dict(centroid, dim, number_clust):
    list = []
    if dim == '2D':
        for i in range(len(centroid[0])):
            slo = {}
            slo = dict([('x0', centroid[0][i]), ('x1', centroid[1][i])])
            list.append(slo)
    elif dim == '3D':
        for i in range(len(centroid[0])):
            slo = {}
            slo = dict([('x0', centroid[0][i]), ('x1', centroid[1][i]), ('x2', centroid[2][i])])
            list.append(slo)
    return json.dumps(list)

def read_data(data, dimension):
    points = []
    x1 = []
    y1 = []
    if dimension == '2D':
        for i in range(len(data)): 
            x1.append(float(data[i]["x0"]))
            y1.append(float(data[i]["x1"]))
        points.append(x1)
        points.append(y1)
    elif dimension == '3D':
        z1 = []
        for i in range(len(data)): 
            x1.append(float(data[i]["x0"]))
            y1.append(float(data[i]["x1"]))
            z1.append(float(data[i]["x2"]))
        points.append(x1)
        points.append(y1)
        points.append(z1)
    return points

def new_txt():
    f = open("poradi.txt", "a+")
    f.write("end")
    f.close()
    f = open("poradi.txt", "r")
    x = f.readline()
    f.close()
    if x == "end":
        f = open("poradi.txt", "w")
        f.write(str(0) + "\n")
        f.close()
    f = open("poradi.txt", "r+")
    x = f.readline()
    x1 = int(x, 10)
    f.close()
    f = open("poradi.txt", "w")
    x1 += 1
    f.write(str(x1) + "\n")
    f.close()
    return x1 - 1

def text_out_3d(x1, x2, y, poradi):
    f = open("result_" + str(poradi) + ".txt","a")
    f.write("(" + str(x1) + "; " + str(x2) + "; " + str(y) + ")\n")
    f.close()

def text_out_2d(x1, x2, poradi):
    f = open("result_" + str(poradi) + ".txt","a")
    f.write("(" + str(x1) + "; " + str(x2) + "; " + ")\n")
    f.close()

def text_out_headline(name, shape, number_cent, poradi):
    f = open("result_" + str(poradi) + ".txt","a")
    f.write("--------------------------------------------------------- Centroid -------------------------------------------------------------\n")
    f.write("File name: " + str(name) + ",   Shape of searched field: " + str(shape) + ",   Numbers of centroids: " + str(number_cent) + "\n")
    f.write("----------------------------------------------------------------------------------------------------------------------\n")
    f.close() 

def text_out_finish(iter, poradi):
    f = open("result_" + str(poradi) + ".txt","a")
    f.write("----------------------------------------------------------------------------------------------------------------------\n")
    f.write("Number of iteration: " + str(iter))
    f.write("\n----------------------------------------------------------------------------------------------------------------------\n")
    f.close() 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.layout = layout(app)
callbacks(app)
if __name__ == '__main__':
    app.run_server(debug=True)