import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__, external_stylesheets=['assets/style.css'])

app.layout = html.Div(
  children=[
    html.Div(
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
                options=[
                  {'label': 'Cases over time', 'value': 'cot'},
                  {'label': 'Tests over time', 'value': 'tot'}
                ],
                value='cot'
              )
            ]),
            html.Div([
              dcc.Dropdown(
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
          className='two columns div-user-controls',
          children=[
            html.P('aaaa')
          ]
        ),          
      ])
  ])

if __name__ == '__main__':
    app.run_server(debug=True)