from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "huma_secret"

# Temporary database
users = {}

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        users[email] = {"password": password, "role": role}

        return redirect("/login")

    return render_template("register.html")

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users and users[email]["password"] == password:
            session["user"] = email
            session["role"] = users[email]["role"]

            if session["role"] == "admin":
                return redirect("/admin")
            else:
                return redirect("/user")

        return "Invalid Credentials"

    return render_template("login.html")

# User Dashboard
@app.route("/user")
def user_dashboard():
    if "user" in session and session["role"] == "user":
        return render_template("user_dashboard.html", email=session["user"])
    return redirect("/login")

# Admin Dashboard
@app.route("/admin")
def admin_dashboard():
    if "user" in session and session["role"] == "admin":
        return render_template("admin_dashboard.html", email=session["user"])
    return redirect("/login")

# Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)