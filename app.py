import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import flask

# Пользователи
USERS = {
    'aizhan': {'name': 'Айжан', 'role': 'employee'},
    'natasha': {'name': 'Наташа', 'role': 'employee'},
    'admin': {'name': 'admin', 'role': 'superuser'},
}

# Загрузка Excel
df = pd.read_excel('df.xlsx')
# print(df)
# Dash app
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H2(id='user-display', style={'textAlign': 'center'}),
    html.Div(
        dcc.Graph(id='revenue-chart'),
        style={
            'width': '80%',        # ширина графика
            'maxWidth': '900px',   # максимальная ширина
            'margin': '0 auto'     # центрирование
        }
    )
])

def get_user():
    return flask.request.args.get('user', 'aizhan')

@app.callback(
    Output('user-display', 'children'),
    Output('revenue-chart', 'figure'),
    Input('revenue-chart', 'id')  # просто триггерим при загрузке
)
def update_output(_):
    user_key = get_user()
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
    app.run_server(debug=True)
