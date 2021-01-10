import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from corona.data import source

app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

app.layout = html.Div(
  children=[
    html.Div(
      # left panel (option panel)
      className='col',
      style={'width': '100%', 'height': '100%'},
      children=[
        html.Div(
          className='four columns div-user-controls',
          children=[
            html.H1('COVID-19 tracking'),
            html.P('As of Jan 2021'),
            html.Div([
              dcc.Dropdown(
                id='mode',
                options=[
                  {'label': 'Case vs Recovery', 'value': 'cvr'},
                  {'label': 'Test vs Case', 'value': 'tvc'}
                ],
                value='cvr'
              )
            ]),
            html.Div(
              style={'margin-top': '10px'},
              children=[
                dcc.Dropdown(
                  id='country',
                  options=[
                    {'label': 'Germany', 'value': 'de'},
                    {'label': 'France', 'value': 'fr'},
                    {'label': 'UK', 'value': 'uk'},
                    {'label': 'USA', 'value': 'us'},
                    {'label': 'China', 'value': 'cn'},
                    {'label': 'Thailand', 'value': 'th'}
                  ],
                  value=['de'],
                  multi=True
                )
            ])
          ]
        ), 
        html.Div(
          # Right panel (graph display)
          id='display',
          className='two columns div-user-controls'
        ),
      ])
  ])

# Data on memory
df_covid19 = source.read_covid19_data()

# Bind UI callbacks 
@app.callback(
  Output(component_id='display', component_property='children'),
  Input(component_id='mode', component_property='value'),
  Input(component_id='country', component_property='value'))
def refresh_display(mode, country):
  print('-------------------------------')
  print(f'Selected mode    : {mode}')
  print(f'Selected country : {country}')
  pass



if __name__ == '__main__':
    print(df_covid19[5:])
    app.run_server(debug=True)