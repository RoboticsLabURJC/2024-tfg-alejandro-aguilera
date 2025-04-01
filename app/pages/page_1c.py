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

def get_country_avg_duration():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT country, 
                   SUM(duration) AS total_duration, 
                   COUNT(*) AS session_count 
            FROM public.log_session
            WHERE country IS NOT NULL  and duration > 0
            GROUP BY country
            HAVING COUNT(*) > 0  
            ORDER BY total_duration DESC;
        """
        df = pd.read_sql(query, conn)
        conn.close()

        df["avg_duration"] = df["total_duration"] / df["session_count"]

        return df[["country", "avg_duration"]]
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["country", "avg_duration"])

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/1c/",
        name="dashboard_1c"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("🌍 Dashboard 1C: Mapa de Duración Promedio de Sesión por País", className="title-large"),

        dcc.Graph(id="world-map", style={"height": "80vh"}),

        html.A("⬅️ Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("world-map", "figure"),
        Input("world-map", "id")
    )
    def update_map(_):
        df = get_country_avg_duration()

        if df.empty:
            return px.choropleth(
                title="No hay datos disponibles",
                locations=[],
                color=[],
            )


        fig = px.choropleth(
            df,
            locations="country",
            locationmode="country names",
            color="avg_duration",
            hover_name="country",
            color_continuous_scale=["#F0F0F0", "#440154", "#21908D", "#FDE725"],
            title="Duración Promedio de Sesión por País",
            labels={"avg_duration": "Duración Promedio (segundos)"}
        )

        fig.update_layout(
            geo=dict(
                showcoastlines=True,
                projection_type="natural earth",
                fitbounds="locations"
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(title="Duración Promedio (segundos)"),
        )

        return fig

    return server
