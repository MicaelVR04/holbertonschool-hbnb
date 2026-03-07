from app import create_app

app = create_app()


@app.route("/")
def hello():
    return "HBnB Project is Running!"


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))
