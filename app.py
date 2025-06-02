import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.express as px
import urllib.parse

USERS = {
    'aizhan': {'name': 'Айжан', 'role': 'employee'},
    'natasha': {'name': 'Наташа', 'role': 'employee'},
    'ruslan': {'name': 'Руслан', 'role': 'superuser'},
}

df = pd.read_excel('df.xlsx')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # добавляем для получения URL
    html.H2(id='user-display', style={'textAlign': 'center'}),
    html.Div(
        dcc.Graph(id='revenue-chart'),
        style={'width': '80%', 'maxWidth': '900px', 'margin': '0 auto'}
    )
])

@app.callback(
    Output('user-display', 'children'),
    Output('revenue-chart', 'figure'),
    Input('url', 'search')  # параметр query string из URL
)
def update_output(search):
    # search будет строкой вида "?user=natasha" или None
    if search:
        query_params = urllib.parse.parse_qs(search.lstrip('?'))
        user_key = query_params.get('user', ['aizhan'])[0]
    else:
        user_key = 'aizhan'

    user_info = USERS.get(user_key, USERS['aizhan'])
    username = user_info['name']
    role = user_info['role']

    if role == 'superuser':
        filtered_df = df
    else:
        filtered_df = df[df['сотрудник'] == username]

    grouped = filtered_df.groupby(['месяц', 'клиент'])['выручка'].sum().reset_index()

    fig = px.bar(
        grouped,
        x='месяц', y='выручка', color='клиент',
        title='Выручка по месяцам',
        labels={'месяц': 'Месяц', 'выручка': 'Выручка, ₽'},
        barmode='stack'
    )

    return f"Вы вошли как: {username}", fig

if __name__ == '__main__':
    app.run(debug=True)
