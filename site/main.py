from flask import Flask, render_template
from os import getcwd, listdir, path

app = Flask(__name__)

articles_dir = f"{getcwd()}/articles/"
categories = [directory for directory in listdir(articles_dir) if path.isdir(path.join(articles_dir, directory))]

@app.route("/")
def home():
    return render_template("index.html", categories=categories)

if __name__ == "__main__":
    app.run(debug=True)