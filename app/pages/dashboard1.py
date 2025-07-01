import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import psycopg2

DB_CONFIG = {
    "dbname": "academy_db",
    "user": "user-dev",
    "password": "unibotics-dev",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_user_exercise_data(username):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT exercise, SUM(duration) as total_duration
            FROM public.log_exercises
            WHERE username = %s
            GROUP BY exercise
            HAVING SUM(duration) > 200  
            ORDER BY total_duration DESC;
        """
        df = pd.read_sql(query, conn, params=[username])
        conn.close()
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["exercise", "total_duration"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/1a/",
        name="dashboard_1a"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("Duración de cada ejercicio por usuario", className="title-large"),
        dcc.Input(
            id="username-input",
            type="text",
            placeholder="Introduce el nombre de usuario...",
            debounce=True,
            className="input-box"
        ),
        dcc.Graph(id="exercise-duration-graph", className="responsive-graph"),
        html.A("Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("exercise-duration-graph", "figure"),
        Input("username-input", "value")
    )
    def update_graph(username):
        if not username:
            return go.Figure(layout={"title": "Introduce un nombre de usuario para ver datos"})

        df = get_user_exercise_data(username)

        if df.empty:
            return go.Figure(layout={"title": f"No se encontraron datos para '{username}'"})

        fig = go.Figure()

        for _, row in df.iterrows():
            fig.add_shape(
                type="line",
                x0=0, x1=row["total_duration"],
                y0=row["exercise"], y1=row["exercise"],
                line=dict(color="gray", width=1)
            )

        fig.add_trace(go.Scatter(
            x=df["total_duration"],
            y=df["exercise"],
            mode="markers",
            marker=dict(size=12, color="red"),
            name="Duración"
        ))

        fig.update_layout(
            title={
                "text": f"Duración Total por Ejercicio - {username}",
                "font": dict(size=28, family="Arial", color="black")
            },
            xaxis_title="Duración Total (segundos)",
            yaxis_title="Ejercicio",
            font=dict(
                family="Arial",
                size=18,
                color="black"
            ),
            xaxis=dict(
                title_font=dict(size=20, color="black"),
                tickfont=dict(size=16)
            ),
            yaxis=dict(
                title_font=dict(size=20, color="black"),
                tickfont=dict(size=16),
                categoryorder="total ascending"
            ),
            plot_bgcolor="white",
            autosize=True,
            height=800,
            margin=dict(l=50, r=50, t=60, b=50)
        )

        return fig

    return server
