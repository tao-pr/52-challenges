import dash
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div(
  children=[
    html.Div(
      className='row',
      children=[
        html.Div(
          className='four columns div-user-controls bg-grey',
          children=[
            html.H2('COVID-19 tracking'),
            html.P('foobar')
          ]
        ), 
        html.Div(
          className='two columns div-user-controls'),
      ])
  ])

if __name__ == '__main__':
    app.run_server(debug=True)