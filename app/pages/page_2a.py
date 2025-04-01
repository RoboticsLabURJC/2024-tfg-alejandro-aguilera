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

def get_country_duration_data():
    """Consulta la base de datos para obtener la duración total de sesiones por país."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT country, SUM(duration) as total_duration
            FROM public.log_session
            WHERE country IS NOT NULL  -- Asegurar que no haya valores nulos
            GROUP BY country
            HAVING SUM(duration) > 0  -- Excluir países con duración 0
            ORDER BY total_duration DESC;
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error al conectar a la BD: {e}")
        return pd.DataFrame(columns=["country", "total_duration"])

def init_dashboard(server):
    """Crear la app Dash e integrarla con Flask"""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix="/2a/",
        name="dashboard_2a"
    )

    dash_app.layout = html.Div(className="dashboard-container", children=[
        html.H1("🌍 Dashboard 2A: Mapa de Duración de Sesiones por País", className="title-large"),

        dcc.Graph(id="world-map", style={"height": "80vh"}),

        html.A("⬅️ Volver al menú", href="/", className="back-link")
    ])

    @dash_app.callback(
        Output("world-map", "figure"),
        Input("world-map", "id")
    )
    def update_map(_):
        df = get_country_duration_data()

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
            color="total_duration",
            hover_name="country",
            color_continuous_scale=["#F0F0F0", "#440154", "#21908D", "#FDE725"],  # De gris claro a colores fuertes
            title="Duración Total de Sesiones por País",
            labels={"total_duration": "Duración Total (segundos)"}
        )

        fig.update_layout(
            geo=dict(
                showcoastlines=True,
                projection_type="natural earth",
                fitbounds="locations"
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(title="Duración Total (segundos)"),
        )

        return fig

    return server
