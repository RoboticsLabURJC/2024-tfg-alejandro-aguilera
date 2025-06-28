import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import psycopg2
import numpy as np

DB_CONFIG = {
    "dbname": "academy_db",
    "user": "user-dev",
    "password": "unibotics-dev",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_session_durations_per_exercise():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT exercise, duration
            FROM public.log_exercises
            WHERE duration > 0
            ORDER BY exercise;
        """
        df = pd.read_sql(query, conn)
        conn.close()

        df["log_duration"] = np.log(df["duration"])
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["exercise", "duration", "log_duration"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/3c/",
        name="dashboard_3c"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("Distribución del tiempo de sesión por usuario en cada ejercicio", className="title-large"),

        dcc.Graph(id="boxplot-log-duration", className="graph-boxplot"),

        html.A("Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("boxplot-log-duration", "figure"),
        Input("boxplot-log-duration", "id")
    )
    def update_boxplot(_):
        df = get_session_durations_per_exercise()

        if df.empty:
            return px.box(title="No hay datos disponibles")

        fig = px.box(
            df,
            x="exercise",
            y="log_duration",
            points="all",
            title="Distribución log(Duración por Sesión) por Ejercicio",
            labels={"exercise": "Ejercicio", "log_duration": "log(Duración por Sesión) (segundos)"},
            color_discrete_sequence=["#6f42c1"]
        )

        fig.update_layout(
            title=dict(
                text="Distribución log(Duración por Sesión) por Ejercicio",
                font=dict(size=24)
            ),
            xaxis=dict(
                title=dict(
                    text="Ejercicio",
                    font=dict(size=20)
                ),
                tickfont=dict(size=16),
                tickangle=-30
            ),
            yaxis=dict(
                title=dict(
                    text="log(Duración por Sesión)",
                    font=dict(size=20)
                ),
                tickfont=dict(size=16)
            ),
            legend=dict(
                font=dict(size=14)
            ),
            plot_bgcolor="white",
            autosize=True,
            height=800,
            margin=dict(l=60, r=40, t=60, b=100)
        )

        return fig

    return server