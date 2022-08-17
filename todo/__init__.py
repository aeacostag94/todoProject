import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        #Las cookies del aplicativo.
        SECRET_KEY="mikey",

        #Se define la base de datos.
        DATABASE_HOST=os.environ.get("FLASK_DATABASE_HOST"),
        DATABASE_PASSWORD=os.environ.get("FLASK_DATABASE_PASSWORD"),
        DATABASE_USER=os.environ.get("FLASK_DATABASE_USER"),
        DATABASE=os.environ.get("FLASK_DATABASE")
    )

    #llamo a la base de datos que se creo en el archivo db.py
    from.import db
    db.init_app(app)

    from . import auth
    from .import todo
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)

    #RUTA DE PRUEBAS
    #TODO cambiar la funcion de hola a funcion de Prueba, solo el nombre
    @app.route("/hola")
    def hola():
        return "Chanchito feliz"
    
    return app
