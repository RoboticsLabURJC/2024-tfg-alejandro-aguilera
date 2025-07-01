import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import numpy as np

DB_CONFIG = {
    "dbname": "academy_db",
    "user": "user-dev",
    "password": "unibotics-dev",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_exercise_list():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT DISTINCT e.exercise_id
            FROM public.exercises e
            WHERE EXISTS (
                SELECT 1
                FROM public.log_exercises le
                WHERE le.exercise = e.exercise_id
                AND le.duration > 0
            )
            ORDER BY e.exercise_id;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return sorted(df["exercise_id"].unique())
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return []

def get_exercise_duration_distribution(exercise_id):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT username, SUM(duration) as total_duration
            FROM public.log_exercises
            WHERE exercise = %s
            GROUP BY username
            HAVING SUM(duration) > 200
            ORDER BY total_duration;
        """
        df = pd.read_sql(query, conn, params=[exercise_id])
        conn.close()

        df["log_duration"] = np.log(df["total_duration"])
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["username", "total_duration", "log_duration"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/3a/",
        name="dashboard_3a"
    )

    exercise_options = [{"label": ex, "value": ex} for ex in get_exercise_list()]

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("Distribución de frecuencia de usuarios con similar duración total por ejercicio", className="title-large"),

        dcc.Dropdown(
            id="exercise-dropdown",
            options=exercise_options,
            placeholder="Selecciona un ejercicio...",
            className="dropdown-box"
        ),

        dcc.Graph(id="log-histogram", className="responsive-graph"),

        html.A("Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("log-histogram", "figure"),
        Input("exercise-dropdown", "value")
    )
    def update_histogram(exercise_id):
        if not exercise_id:
            fig = go.Figure()
            fig.update_layout(title_text="Selecciona un ejercicio para ver datos")
            return fig

        df = get_exercise_duration_distribution(exercise_id)

        if df.empty:
            fig = go.Figure()
            fig.update_layout(title_text=f"No hay datos para '{exercise_id}'")
            return fig

        fig = px.histogram(
            df,
            x="log_duration",
            nbins=30,
            title=f"Distribución Logarítmica de Duraciones - {exercise_id}",
            labels={"log_duration": "log(Duración Total)", "count": "Número de Usuarios"},
            color_discrete_sequence=["#17a2b8"]
        )

        fig.update_layout(
            title=dict(
                text=f"Distribución Logarítmica de Duraciones - {exercise_id}",
                font=dict(size=24)
            ),
            xaxis=dict(
                title=dict(
                    text="log(Duración Total en segundos)",
                    font=dict(size=20)
                ),
                tickfont=dict(size=16)
            ),
            yaxis=dict(
                title=dict(
                    text="Número de Usuarios",
                    font=dict(size=20)
                ),
                tickfont=dict(size=16)
            ),
            legend=dict(
                font=dict(size=14)
            ),
            plot_bgcolor="white",
            bargap=0.1,
            autosize=True,
            height=800,
            margin=dict(l=60, r=40, t=60, b=60)
        )

        return fig

    return server
