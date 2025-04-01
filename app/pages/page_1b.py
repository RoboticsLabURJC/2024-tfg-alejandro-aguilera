import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import psycopg2

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
        query = "SELECT DISTINCT exercise_id FROM public.exercises ORDER BY exercise_id;"
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
            HAVING SUM(duration) > 0  
            ORDER BY total_duration;
        """
        df = pd.read_sql(query, conn, params=[exercise_id])
        conn.close()
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["username", "total_duration"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/1b/",
        name="dashboard_1b"
    )

    exercise_options = [{"label": ex, "value": ex} for ex in get_exercise_list()]

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("📊 Dashboard 1B: Frecuencia de Usuarios por Duración"),

        dcc.Dropdown(
            id="exercise-dropdown",
            options=exercise_options,
            placeholder="Selecciona un ejercicio...",
            className="dropdown-box"
        ),

        dcc.Graph(id="exercise-histogram"),

        html.A("⬅️ Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("exercise-histogram", "figure"),
        Input("exercise-dropdown", "value")
    )
    def update_histogram(exercise_id):
        if not exercise_id:
            return px.histogram(title="Selecciona un ejercicio para ver datos")

        df = get_exercise_duration_distribution(exercise_id)

        if df.empty:
            return px.histogram(
                title=f"No hay datos para '{exercise_id}'",
                x=[],
                nbins=30
            )

        fig = px.histogram(
            df,
            x="total_duration",
            nbins=30,  # Número de barras en el histograma
            title=f"Distribución de Duraciones - {exercise_id}",
            labels={"total_duration": "Duración Total (segundos)", "count": "Número de Usuarios"},
        )

        fig.update_layout(
            xaxis_title="Duración Total (segundos)",
            yaxis_title="Número de Usuarios",
            plot_bgcolor="white"
        )

        return fig

    return server
