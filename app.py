from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "huma_secret"

users = {}

artworks = [
{
"id":0,
"title":"Sunset Painting",
"artist":"Ravi Kumar",
"description":"Beautiful sunset artwork",
"category":"Painting",
"image":"https://via.placeholder.com/200",
"price":5000,
"is_available":True
},
{
"id":1,
"title":"Modern Sculpture",
"artist":"Anita Shah",
"description":"Abstract sculpture artwork",
"category":"Sculpture",
"image":"https://via.placeholder.com/200",
"price":8000,
"is_available":True
},
{
"id":2,
"title":"Nature Art",
"artist":"Rahul Mehta",
"description":"Nature inspired painting",
"category":"Painting",
"image":"https://via.placeholder.com/200",
"price":3500,
"is_available":True
}
]

@app.route("/")
def home():
    search = request.args.get("search")
    artist = request.args.get("artist")
    category = request.args.get("category")

    filtered_artworks = artworks

    if search:
        filtered_artworks = [a for a in filtered_artworks if search.lower() in a["title"].lower()]

    if artist:
        filtered_artworks = [a for a in filtered_artworks if artist.lower() in a["artist"].lower()]

    if category:
        filtered_artworks = [a for a in filtered_artworks if category.lower() in a["category"].lower()]

    return render_template("home.html", artworks=filtered_artworks)

@app.route("/artwork/<int:id>")
def artwork_detail(id):
    for art in artworks:
        if art["id"] == id:
            return render_template("artwork_detail.html", artwork=art)
    return "Artwork not found"

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        users[email] = {
        "password":password,
        "role":role,
        "is_active":True
        }

        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        if email in users and users[email]["password"] == password:

            if users[email]["is_active"] == False:
                return "Account Disabled"

            session["user"] = email
            session["role"] = users[email]["role"]

            if session["role"] == "admin":
                return redirect("/admin")

            else:
                return redirect("/user")

        return "Invalid Credentials"

    return render_template("login.html")

@app.route("/user")
def user_dashboard():
    if "user" in session and session["role"] == "user":
        return "Welcome User"
    return redirect("/login")

@app.route("/admin")
def admin_dashboard():
    if "user" in session and session["role"] == "admin":

        return render_template(
        "admin_dashboard.html",
        email=session["user"],
        users=users
        )

    return redirect("/login")

@app.route("/change_role/<email>")
def change_role(email):

    if session.get("role") != "admin":
        return "Unauthorized"

    if users[email]["role"] == "user":
        users[email]["role"] = "admin"
    else:
        users[email]["role"] = "user"

    return redirect("/admin")

@app.route("/toggle_status/<email>")
def toggle_status(email):

    if session.get("role") != "admin":
        return "Unauthorized"

    users[email]["is_active"] = not users[email]["is_active"]

    return redirect("/admin")

@app.route("/artworks")
def artworks_page():

    if session.get("role") != "admin":
        return "Unauthorized"

    return render_template("artworks.html", artworks=artworks)

@app.route("/add_artwork", methods=["GET","POST"])
def add_artwork():

    if session.get("role") != "admin":
        return "Unauthorized"

    if request.method == "POST":

        title = request.form["title"]
        artist = request.form["artist"]
        price = request.form["price"]
        category = request.form["category"]

        artworks.append({
        "id":len(artworks),
        "title":title,
        "artist":artist,
        "description":"New artwork added",
        "category":category,
        "image":"https://via.placeholder.com/200",
        "price":price,
        "is_available":True
        })

        return redirect("/artworks")

    return render_template("add_artwork.html")

@app.route("/delete_artwork/<int:id>")
def delete_artwork(id):

    if session.get("role") != "admin":
        return "Unauthorized"

    artworks.pop(id)

    return redirect("/artworks")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)