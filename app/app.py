from flask import Flask, render_template
import pages.page_1a as page_1a
import pages.page_1b as page_1b
import pages.page_1c as page_1c
import pages.page_2a as page_2a
import pages.page_2b as page_2b
import pages.page_2c as page_2c
import pages.page_3a as page_3a
import pages.page_3b as page_3b
import pages.page_3c as page_3c

app = Flask(__name__)

app = page_1a.init_dashboard(app)
app = page_1b.init_dashboard(app)
app = page_1c.init_dashboard(app)
app = page_2a.init_dashboard(app)
app = page_2b.init_dashboard(app)
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
