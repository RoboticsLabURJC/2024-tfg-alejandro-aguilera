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

def get_sessions_per_month(year):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT 
                DATE_TRUNC('month', s.start_date) AS month,
                COUNT(*) AS total_sessions,
                COUNT(CASE WHEN u.gender = 'F' THEN 1 END) AS female_sessions,
                COUNT(CASE WHEN u.gender = 'M' THEN 1 END) AS male_sessions
            FROM public.log_session s
            JOIN public.common_user u ON s.username = u.username
            WHERE EXTRACT(YEAR FROM s.start_date) = %s
            GROUP BY month
            ORDER BY month;
        """
        df = pd.read_sql(query, conn, params=[year])
        conn.close()

        df["month"] = df["month"].dt.strftime("%B")
        df["month"] = pd.Categorical(df["month"], categories=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ], ordered=True)

        return df.sort_values("month")
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["month", "total_sessions", "female_sessions", "male_sessions"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/2c/",
        name="dashboard_2c"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("Sesiones por Mes", className="title-large"),

        dcc.Dropdown(
            id="year-selector",
            options=[{"label": str(y), "value": y} for y in range(2021, 2026)],
            value=2024,
            clearable=False,
            className="dropdown"
        ),

        dcc.Graph(id="sessions-line-chart", className="responsive-graph"),

        html.A("Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("sessions-line-chart", "figure"),
        Input("year-selector", "value")
    )
    def update_line_chart(selected_year):
        df = get_sessions_per_month(selected_year)

        if df.empty:
            return go.Figure(layout={"title": f"No hay datos disponibles para {selected_year}"})

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df["month"],
            y=df["total_sessions"],
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=3),
            name="Total Sesiones",
        ))

        fig.add_trace(go.Scatter(
            x=df["month"],
            y=df["female_sessions"],
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=3),
            name="Sesiones Femeninas"
        ))

        fig.add_trace(go.Scatter(
            x=df["month"],
            y=df["male_sessions"],
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=3),
            name="Sesiones Masculinas"
        ))

        fig.update_layout(
            title=dict(
                text=f"Número de Sesiones por Mes en {selected_year}",
                font=dict(size=24)
            ),
            xaxis=dict(
                title=dict(
                    text="Mes",
                    font=dict(size=20)
                ),
                tickfont=dict(size=16)
            ),
            yaxis=dict(
                title=dict(
                    text="Número de Sesiones",
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
            margin=dict(l=60, r=40, t=60, b=60)
        )

        return fig

    return server
