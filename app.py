from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "huma_secret"

# Temporary databases
users = {}
artworks = []

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Register
@app.route("/register", methods=["GET","POST"])
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


# Login
@app.route("/login", methods=["GET","POST"])
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
        return render_template("admin_dashboard.html", email=session["user"], users=users)

    return redirect("/login")


# Change Role
@app.route("/change_role/<email>")
def change_role(email):

    if session.get("role") != "admin":
        return "Unauthorized"

    if users[email]["role"] == "user":
        users[email]["role"] = "admin"
    else:
        users[email]["role"] = "user"

    return redirect("/admin")


# Toggle User Status
@app.route("/toggle_status/<email>")
def toggle_status(email):

    if session.get("role") != "admin":
        return "Unauthorized"

    users[email]["is_active"] = not users[email]["is_active"]

    return redirect("/admin")


# =============================
# ARTWORK MANAGEMENT MODULE
# =============================

# View Artworks
@app.route("/artworks")
def artworks_page():

    if session.get("role") != "admin":
        return "Unauthorized"

    return render_template("artworks.html", artworks=artworks)


# Add Artwork
@app.route("/add_artwork", methods=["GET","POST"])
def add_artwork():

    if session.get("role") != "admin":
        return "Unauthorized"

    if request.method == "POST":

        title = request.form["title"]
        artist = request.form["artist"]
        price = request.form["price"]

        artwork = {
            "title": title,
            "artist": artist,
            "price": price,
            "sold": False
        }

        artworks.append(artwork)

        return redirect("/artworks")

    return render_template("add_artwork.html")


# Delete Artwork
@app.route("/delete_artwork/<int:index>")
def delete_artwork(index):

    if session.get("role") != "admin":
        return "Unauthorized"

    artworks.pop(index)

    return redirect("/artworks")


# Logout
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)