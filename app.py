# see https://plotly.com/python/line-charts/
# see https://dash.plotly.com/live-updates
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import os
import io
import requests
import time

import config


# Load data
def load_data():
    global df, last_load_data

    if (int(time.time()) - last_load_data) > (1 * 60):
        last_load_data = int(time.time())
        req = requests.get(config.DATASET_RAW_CSV_URL)
        if req.status_code != 200:
            print(f"WTF ??? {req.status_code} {req.reason} {req.text}")
        data = req.text
        buffer = io.StringIO(data)
        df = pd.read_csv(buffer, parse_dates=True)
        df['data'] = pd.to_datetime(df['data'])


df = None
last_load_data = 0
load_data()

external_scripts = [
    {
        'data-goatcounter': 'https://covidvillarosa.goatcounter.com/count',
        'async src': '//gc.zgo.at/count.js'
    }
]

# Initialise the app
app = dash.Dash(__name__, external_scripts=external_scripts)


def get_line_figure_from_keys(keys, title, color):
    fig = go.Figure()
    color.reverse()
    for k in keys:
        fig.add_trace(go.Scatter(x=df['data'], y=df[k], name=k, line=dict(color=color.pop())))
    fig.layout = dict(
        title=title,
        showlegend=True,
        legend=dict(
            x=0.05,
            y=1.0
        ),
        margin=dict(l=40, r=0, t=40, b=30),
        xaxis_tickformat='%d %b',
    )
    fig.update_yaxes(nticks=20, linecolor='black')
    fig.update_xaxes(linecolor='black')
    fig.update_layout({'plot_bgcolor': 'rgba(240, 240, 240, 1)', 'paper_bgcolor': 'rgba(240, 240, 240, 1)'})
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode='x')
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    return fig


def get_bar_figure(data, title, legend_name, color):
    fig = go.Figure()
    for k in range(len(legend_name)):
        fig.add_trace(go.Bar(x=df['data'], y=data[k], name=legend_name[k], text=data[k],
                             textposition='auto', marker_color=color[k]))
    fig.layout = dict(
        title=title,
        showlegend=True,
        legend=dict(
            x=0.05,
            y=1.0
        ),
        margin=dict(l=40, r=0, t=40, b=30),
        xaxis_tickformat='%d %b',
    )
    fig.update_yaxes(nticks=20, linecolor='black')
    fig.update_xaxes(linecolor='black')
    fig.update_layout({'plot_bgcolor': 'rgba(240, 240, 240, 1)', 'paper_bgcolor': 'rgba(240, 240, 240, 1)'})
    fig.update_traces(hovertemplate='%{y}')
    fig.update_layout(hovermode='x', barmode='group')
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    return fig


def get_last_value(key):
    delta_tmp = df[key].tail(2).to_list()
    return {'value': int(df[key].tail(1)), 'delta_giornaliero': delta_tmp[1] - delta_tmp[0]}


def get_daily_variations(key):
    tmp = df[key].to_list()
    variations = [tmp[0]]
    for i in range(1, len(tmp)):
        variations.append(tmp[i] - tmp[i - 1])
    return variations


def delta_html(delta):
    if delta >= 0:
        return html.Footer(f"+{delta} rispetto a ieri", className='green'),
    else:
        return html.Footer(f"{delta} rispetto a ieri", className='red'),


def serve_layout():
    global df

    load_data()
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src=app.get_asset_url(config.LOGO_PATH),
                                id="logo-comune",
                                style={
                                    "height": "100px",
                                    "width": "auto",
                                    "margin-bottom": "25px",
                                },
                            )
                        ],
                        className="one-third column",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        f"Covid-19 {config.CITY_NAME}",
                                        style={"margin-bottom": "0px"},
                                    ),
                                    html.H5(
                                        "Dashboard", style={"margin-top": "0px"}
                                    ),
                                ]
                            )
                        ],
                        className="one-half column",
                        id="title",
                    ),
                    html.Div(
                        [
                            html.A(
                                html.Button(config.MAYOR_NAME, id="learn-more-button"),
                                href=config.MAYOR_LINK,
                            ),
                        ],
                        className="one-third column",
                        id="button",
                    ),
                ],
                id="header",
                className="row flex-display",
                style={"margin-bottom": "25px"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            *config.DASHBOARD_DESCRIPTION,
                            html.H6(f"Dati aggiornati al {df['data'].tail(1).to_list()[0].strftime('%d/%m/%Y')}"),
                            html.Div(
                                [
                                    html.Div(
                                        [html.H6(get_last_value('positivi')['value']),
                                         html.P("Positivi"),
                                         html.Div(delta_html(get_last_value('positivi')['delta_giornaliero']))],
                                        id="positivi_attuali",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(get_last_value('quarantena')['value']), html.P("In Quarantena"),
                                         html.Div(delta_html(get_last_value('quarantena')['delta_giornaliero']))],
                                        id="quarantena_attuali",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(get_last_value('guariti')['value']), html.P("Guariti"),
                                         html.Div(delta_html(get_last_value('guariti')['delta_giornaliero']))],
                                        id="guariti_attuali",
                                        className="mini_container",
                                    ),
                                    html.Div(
                                        [html.H6(get_last_value('decessi')['value']), html.P("Decessi"),
                                         html.Div(delta_html(get_last_value('decessi')['delta_giornaliero']))],
                                        id="decessi_attuali",
                                        className="mini_container",
                                    ),
                                ],
                                id="info-container",
                                className="row container-display",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(config={'displayModeBar': False},
                                              animate=False,
                                              figure=get_line_figure_from_keys(
                                                  ['positivi', 'quarantena', 'guariti', 'decessi'],
                                                  'Grafico generale variabili',
                                                  ['#C94747', '#1f77b4', '#2ca02c', '#bcbd22']
                                              ))
                                ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(config={'displayModeBar': False},
                                              animate=False,
                                              figure=get_line_figure_from_keys(
                                                  ['positivi'],
                                                  'Soggetti attualmente positivi', ['#C94747']
                                              )),
                                    html.P('''Nota: Grafico a linee che indica l'andamento dei soggetti 
                                        positivi nel tempo.'''),
                                ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(config={'displayModeBar': False},
                                              animate=False,
                                              figure=get_line_figure_from_keys(
                                                  ['quarantena'],
                                                  'Soggetti attualmente in quarantena', ['#1f77b4']
                                              )),
                                    html.P('''Nota: '''),
                                    html.P('''- Grafico a linee che indica l'andamento dei soggetti 
                                in quarantena nel tempo.'''),
                                    html.P('''- I numeri dei soggetti in quarantena non sono strettamente 
                                correlati ai positivi.''')

                                ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(config={'displayModeBar': False},
                                              animate=False,
                                              figure=get_bar_figure([get_daily_variations('positivi'),
                                                                     get_daily_variations('quarantena')],
                                                                    'Variazione rispetto al giorno precedente',
                                                                    ['positivi', 'quarantena'],
                                                                    ['#C94747', '#1f77b4'])
                                              ),
                                    html.P('''Nota: '''),
                                    html.P('''- Grafico a barre che indica la variazione dei soggetti positivi e
                                in quarantena.'''),
                                    html.P('''- Valori ottenuti tramite la sottrazione dei dati del 
                                giorno(t) - dati giorno(t-1).'''),
                                ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(config={'displayModeBar': False},
                                              animate=False,
                                              figure=get_line_figure_from_keys(
                                                  ['guariti'],
                                                  'Soggetti attualmente guariti', ['#2ca02c']
                                              )),
                                    html.P('''Nota: Grafico a linee che indica l'andamento dei soggetti 
                                        guariti nel tempo.'''),
                                ],
                                className="pretty_container",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(config={'displayModeBar': False},
                                              animate=False,
                                              figure=get_line_figure_from_keys(
                                                  ['decessi'],
                                                  'Decessi', ['#bcbd22']
                                              )),
                                    html.P('''Nota: Grafico a linee che indica l'andamento dei decessi 
                            nel tempo.'''),
                                ],
                                className="pretty_container",
                            ),
                            html.P(
                                config.DASHBOARD_FOOTER
                            )
                        ]
                    )
                ]
            ),
        ]
    )


app.layout = serve_layout

# Run the app
if __name__ == '__main__':
    app.title = f"Covid19{config.CITY_NAME} | Dashboard"
    app.run_server(host='0.0.0.0', debug=os.getenv('DEBUG', False), port=os.getenv('PORT', 8050))
