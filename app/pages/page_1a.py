import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import psycopg2

# Configuración de la base de datos
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
            HAVING SUM(duration) > 0  
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
        html.H1("📊 Dashboard 1A: Análisis de Ejercicios por Usuario"),

        dcc.Input(
            id="username-input",
            type="text",
            placeholder="Introduce el nombre de usuario...",
            debounce=True,
            className="input-box"
        ),

        dcc.Graph(id="exercise-duration-graph"),

        html.A("⬅️ Volver al menú", href="/", className="back-link")
    ])

    # actualizar para nuevo usario
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

        lines = go.Scatter(
            x=df["total_duration"],
            y=df["exercise"],
            mode="lines",
            line=dict(color="gray", width=1),
            showlegend=False
        )

        circles = go.Scatter(
            x=df["total_duration"],
            y=df["exercise"],
            mode="markers",
            marker=dict(size=12, color="red"),
            name="Duración"
        )

        fig = go.Figure()

        for i, row in df.iterrows():
            fig.add_shape(
                type="line",
                x0=0, x1=row["total_duration"],  # Desde el eje Y hasta el punto
                y0=row["exercise"], y1=row["exercise"],  # En la misma posición en Y
                line=dict(color="gray", width=1)
            )

        fig.add_trace(circles)

        fig.update_layout(
            title=f"Duración Total por Ejercicio - {username}",
            xaxis_title="Duración Total (segundos)",
            yaxis_title="Ejercicio",
            plot_bgcolor="white",
            yaxis=dict(categoryorder="total ascending")  # Ordenar de mayor a menor duración
        )

        return fig

    return server
