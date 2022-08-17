import functools
# Set de funciones para crear apps web.

from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)

# *Blueprint, para separ codigo por partes mini apps, *flash envia mensaje a usuarios, *g una variable global que toma X valor, *render_tamplete para renderisar plantillas, *request porque se reciben datos de formulario, *url_for para generar urls y *session para mantener referencias de usuarios

from werkzeug.security import check_password_hash, generate_password_hash

# check_password_hash verificar si una contraseña es igual a otra, generate_password_hash para poder incriptar las contraseñas de nuestros usuarios

from todo.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")
# url_prefix es para concatenar las url que se van generando.

# REGISTRO DE USUARIOS
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute(
            "select id from user where username = %s", (username,)
        )
        if not username:
            error = "Username es requerido"
        if not password:
            error = "Password es requerido"
        elif c.fetchone() is not None:
            error = "Usuario {} se encunetra registrado.".format(username)

        if error is None:
            c.execute(
                "insert into user (username, password) values (%s, %s)",
                # generate password has para encriptar la contraseña
                (username, generate_password_hash(password))
            )
            db.commit()

            return redirect(url_for("auth.login"))

        flash(error)
    return render_template("auth/register.html")

# VERIFICAICON DE USUARIOS
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db, c = get_db()
        error = None
        c.execute(
            "select * from user where username = %s", (username,)
        )
        user = c.fetchone()

        if user is None:
            error = "Usuario y/o contraseña invalidas"
            # Es buena practica no devolver usuarios ni contraseñas en las paginas de login si se presentan errores!!
        elif not check_password_hash(user["password"], password):
            error = "Usuario y/o contraseña invalidas"

        if error is None:
            # si error es nada es decir usuario y password estan bien
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("todo.index"))

        flash(error)
    return render_template("auth/login.html")

#antes de cada peticion se ejecuta.
@bp.before_app_request
def load_logged_in_user():
    user_id=session.get("user_id")

    if user_id is None:
        g.user=None
    else:
        db, c= get_db()
        c.execute (
            "select * from user where id = %s", (user_id,)
        )
        g.user=c.fetchone()
#funcion decoradora recibe la misma funcion que estamos decorando, indica que es una funcioon de vista llamda view
#Se actualiza un comentario.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**Kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        
        return view(**Kwargs)

    return wrapped_view    


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
