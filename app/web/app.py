from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)
app.secret_key = "dev-secret-key"


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if username == "admin" and password == "admin123":
        session["logged_in"] = True
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Invalid credentials")


@app.route("/dashboard")
def dashboard():
    if session.get("logged_in"):
        return render_template("dashboard.html")

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

                    

if __name__ == "__main__":
    app.run(debug=True)