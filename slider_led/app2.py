from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash
import socket

APP_USER = "jonathan"       # Ejemplo: diana
APP_PW_HASH = "scrypt:32768:8:1$7s26umeOpJn47nSp$186b77a13c0f5288df0a19cbdc0fc7e738e99361acd1e617621f4d4a44589c5d48894fa39e0e97d394e69b6fce1164acda7b22d340cf999fae1d065086552056"       # Ejemplo: "scrypt:32768:8:1$...$..."
SECRET_KEY = "root"  # clave larga y aleatoria

TCP_HOST = "127.0.0.1"
TCP_PORT = 5001  # coincide con servidor_tcp2.py

app = Flask(__name__, template_folder="templates2", static_folder="static2", static_url_path="/static")
app.secret_key = SECRET_KEY

def is_logged_in():
    return session.get("logged_in") is True

def send_cmd(cmd: str) -> str:
    with socket.create_connection((TCP_HOST, TCP_PORT), timeout=3) as s:
        s.sendall((cmd + "\n").encode("utf-8"))
        data = b""
        while b"\n" not in data:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        return data.decode("utf-8", errors="ignore").strip()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username", "").strip()
        pw = request.form.get("password", "")
        if user == APP_USER and check_password_hash(APP_PW_HASH, pw):
            session["logged_in"] = True
            return redirect(url_for("index"))
        return render_template("login.html", error="Usuario o contraseña incorrectos")
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
def index():
    if not is_logged_in():
        return redirect(url_for("login"))
    return render_template("index.html")

@app.post("/set_led")
def set_led():
    if not is_logged_in():
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    data = request.get_json(silent=True) or {}
    led = int(data.get("led", 0))
    value = int(data.get("value", 0))

    if led not in (1, 2, 3, 4):
        return jsonify({"ok": False, "error": "Usa led=1..4"}), 400

    if value < 0: value = 0
    if value > 255: value = 255

    cmd = f"LED{led}:{value}"
    resp = send_cmd(cmd)

    return jsonify({"ok": resp.startswith("OK"), "cmd": cmd, "resp": resp})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
