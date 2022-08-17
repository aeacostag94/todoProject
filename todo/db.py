import mysql.connector

import click
# click es una herramienta que ejecuta comandos en la terminal la idea es crear tablas y relaciones desde terminal y no desde workbrench.
from flask import current_app, g
# current app mantiene la aplicacion ejecutando y g es una varible que se le asigna variables, para almacenar usuario
from flask.cli import with_appcontext
# acceder variables de la configiracion en __init__
from .schema import instructions
# schema contiene los scripts de la base de datos


def get_db():
    if"db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DATABASE_HOST"],
            user=current_app.config["DATABASE_USER"],
            password=current_app.config["DATABASE_PASSWORD"],
            database=current_app.config["DATABASE"]
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c

# SE crea una funcion para cuando se temrine una peticion cierra la conexion
def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:  # si db no es none es decir que yo la llame y esta abierta
        db.close()


def init_db():
    db,c=get_db()

    for i in instructions:
        c.execute(i)
    db.commit()

#se crea este comando para llamar a la base de datos desde el terminal
@click.command("init-db") 
@with_appcontext
#funcion para crear base de datos.
def init_db_command():
    init_db() #logica para correr scripts.
    click.echo("Base de datos inicializada")

# funcion para cerrar conexion cuando se temrine la app.
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
