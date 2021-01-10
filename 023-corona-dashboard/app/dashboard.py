import dash
import dash_html_components as html

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
            html.P('foobar')
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