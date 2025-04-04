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

def get_sessions_per_month():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT DATE_TRUNC('month', start_date) AS month, COUNT(*) AS session_count
            FROM public.log_session
            WHERE EXTRACT(YEAR FROM start_date) = 2024
            GROUP BY month
            ORDER BY month;
        """
        df = pd.read_sql(query, conn)
        conn.close()

        df["month"] = df["month"].dt.strftime("%B")
        df["month"] = pd.Categorical(df["month"], categories=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ], ordered=True)

        return df.sort_values("month")
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["month", "session_count"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/2c/",
        name="dashboard_2c"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("Dashboard 2C: Sesiones por Mes en 2024", className="title-large"),

        dcc.Graph(id="sessions-line-chart", className="responsive-graph"),

        html.A("Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("sessions-line-chart", "figure"),
        Input("sessions-line-chart", "id")
    )
    def update_line_chart(_):
        df = get_sessions_per_month()

        if df.empty:
            return go.Figure(layout={"title": "No hay datos disponibles para 2024"})

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["month"],
            y=df["session_count"],
            mode="lines+markers",
            marker=dict(size=12, color="red"),
            line=dict(width=3, color="blue"),
            name="Sesiones"
        ))

        fig.update_layout(
            title="Número de Sesiones por Mes en 2024",
            xaxis_title="Mes",
            yaxis_title="Número de Sesiones",
            plot_bgcolor="white",
        autosize = True,
        height = 800,
        margin = dict(l=0, r=0, t=30, b=0)
        )

        return fig

    return server
