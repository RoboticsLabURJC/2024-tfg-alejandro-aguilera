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

def get_session_duration_distribution():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT duration
            FROM public.log_session
            WHERE duration > 0  
            ORDER BY duration;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["duration"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/2b/",
        name="dashboard_2b"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("📊 Dashboard 2B: Distribución de Duración de Sesiones"),

        dcc.Graph(id="session-histogram"),

        html.A("⬅️ Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("session-histogram", "figure"),
        Input("session-histogram", "id")
    )
    def update_histogram(_):
        df = get_session_duration_distribution()

        if df.empty:
            return px.histogram(
                title="No hay datos disponibles",
                x=[],
            )

        fig = px.histogram(
            df,
            x="duration",
            nbins=30,
            title="Distribución de Duraciones de Sesión",
            labels={"duration": "Duración de Sesión (segundos)", "count": "Número de Usuarios"},
            color_discrete_sequence=["#007bff"]
        )

        fig.update_layout(
            xaxis_title="Duración de Sesión (segundos)",
            yaxis_title="Número de Usuarios",
            plot_bgcolor="white",
            bargap=0.1
        )

        return fig

    return server
