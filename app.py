from flask import Flask, redirect, render_template, request, url_for

import tareas

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("lista_tareas.html", tareas=tareas.listar_tareas())


@app.post("/agregar")
def agregar():
    tareas.agregar_tarea(request.form.get("texto", ""))
    return redirect(url_for("index"))


@app.post("/completar/<int:tarea_id>")
def completar(tarea_id: int):
    tareas.completar_tarea(tarea_id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
