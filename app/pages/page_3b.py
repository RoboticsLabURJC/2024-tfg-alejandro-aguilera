import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import psycopg2
import numpy as np  # Para log(x)

DB_CONFIG = {
    "dbname": "academy_db",
    "user": "user-dev",
    "password": "unibotics-dev",
    "host": "127.0.0.1",
    "port": "5432"
}

def get_all_exercise_duration_distribution():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT exercise, username, SUM(duration) as total_duration
            FROM public.log_exercises
            WHERE duration > 0
            GROUP BY exercise, username
            HAVING SUM(duration) > 0
            ORDER BY exercise;
        """
        df = pd.read_sql(query, conn)
        conn.close()

        df["log_duration"] = np.log(df["total_duration"])
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["exercise", "username", "log_duration"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/3b/",
        name="dashboard_3b"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("📦 Dashboard 3B: Boxplot (log) por Ejercicio", className="title-large"),

        dcc.Graph(id="boxplot-all-exercises", style={"height": "85vh"}),  # Grande

        html.A("⬅️ Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("boxplot-all-exercises", "figure"),
        Input("boxplot-all-exercises", "id")
    )
    def update_boxplot(_):
        df = get_all_exercise_duration_distribution()

        if df.empty:
            return px.box(title="No hay datos disponibles")

        fig = px.box(
            df,
            x="exercise",
            y="log_duration",
            points="all",
            title="Distribución log(Duración) por Usuario y Ejercicio",
            labels={"exercise": "Ejercicio", "log_duration": "log(Duración) (segundos)"},
            color_discrete_sequence=["#17a2b8"]
        )

        fig.update_layout(
            yaxis_title="log(Duración Total por Usuario)",
            xaxis_title="Ejercicio",
            plot_bgcolor="white",
            autosize=True,
            margin=dict(l=40, r=40, t=60, b=150),
            xaxis_tickangle=-30,
            font=dict(size=14)
        )

        return fig

    return server
