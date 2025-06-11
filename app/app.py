from flask import Flask, render_template
import pages.dashboard1 as page_1a
import pages.dashboard2 as page_1c
import pages.dashboard3 as page_2a
import pages.dashboard4 as page_2c
import pages.dashboard5 as page_3a
import pages.dashboard6 as page_3b
import pages.dashboard7 as page_3c

app = Flask(__name__)

app = page_1a.init_dashboard(app)
app = page_1c.init_dashboard(app)
app = page_2a.init_dashboard(app)
app = page_2c.init_dashboard(app)
app = page_3a.init_dashboard(app)
app = page_3b.init_dashboard(app)
app = page_3c.init_dashboard(app)

# Ruta del menú graficas
@app.route("/")
def index():
    return render_template("index.html", active_page="dashboard")

# Ruta para la documentación
@app.route("/documentacion")
def documentacion():
    return render_template("documentacion.html", active_page="documentacion")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
