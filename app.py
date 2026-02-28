from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "huma_secret"

# Temporary in-memory database
users = {}

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("home.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        users[email] = {
            "password": password,
            "role": role,
            "is_active": True
        }

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if email in users:
            if users[email]["password"] == password:
                if users[email]["is_active"]:

                    session["user"] = email
                    session["role"] = users[email]["role"]

                    if session["role"] == "admin":
                        return redirect("/admin")
                    else:
                        return redirect("/user")

                else:
                    return "Account is deactivated"

        return "Invalid Credentials"

    return render_template("login.html")


# ---------------- USER DASHBOARD ----------------
@app.route("/user")
def user_dashboard():
    if "user" in session and session["role"] == "user":
        return render_template("user_dashboard.html", email=session["user"])
    return redirect("/login")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin")
def admin_dashboard():
    if "user" in session and session["role"] == "admin":
        return render_template("admin_dashboard.html", email=session["user"], users=users)
    return redirect("/login")


# ---------------- CHANGE ROLE ----------------
@app.route("/change_role/<email>")
def change_role(email):
    if "user" in session and session["role"] == "admin":
        if email in users:
            if users[email]["role"] == "user":
                users[email]["role"] = "admin"
            else:
                users[email]["role"] = "user"

    return redirect("/admin")


# ---------------- TOGGLE STATUS ----------------
@app.route("/toggle_status/<email>")
def toggle_status(email):
    if "user" in session and session["role"] == "admin":
        if email in users:
            users[email]["is_active"] = not users[email]["is_active"]

    return redirect("/admin")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)