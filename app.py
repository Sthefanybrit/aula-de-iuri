from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = "chave_secreta"  # Chave secreta para as sessões

# Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    return conn

# Página inicial (Login)
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha)).fetchone()
        conn.close()
        if user:
            # Cria uma sessão para o usuário logado
            session["user_id"] = user["id"]
            session["nome"] = user["nome"]
            return redirect(url_for("dashboard"))
        else:
            flash("Login inválido ou usuário não cadastrado. Por favor, cadastre-se primeiro.", "error")
    return render_template("login.html")

# Página de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
        if user:
            flash("E-mail já cadastrado. Faça login.", "error")
        else:
            conn.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
            conn.commit()
            conn.close()
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for("login"))
        conn.close()
    return render_template("cadastro.html")

# Página de dashboard (após login)
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Mostra informações específicas do usuário logado
    user_id = session["user_id"]
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()

    return render_template("dashboard.html", nome=user["nome"], email=user["email"])

# Logout
@app.route("/logout")
def logout():
    session.clear()  # Limpa a sessão do usuário
    flash("Você saiu com sucesso!", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
