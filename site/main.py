from flask import Flask, render_template, request
from os import getcwd, listdir, path
from urllib.parse import quote

app = Flask(__name__)

def get_categotries_and_articles():
    categories_path = f"{getcwd()}/articles/"
    categories = [(categories_name, categories_path + categories_name) for categories_name in listdir(categories_path)]
    
    data = dict()

    for category_name, category_path in categories:
        data[category_name] = [
            {
                "encoded": quote(article_name[:article_name.rfind(".")], safe=""),
                "decoded": article_name[:article_name.rfind(".")]
            }
            for article_name in listdir(category_path)
        ]

    return data

data = get_categotries_and_articles()

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", data=data)

@app.route("/article", methods=['GET'])
def article():
    category = request.args.get('category')
    article_name = request.args.get('article')

    if not category or not article_name:
        return "Category or article not specified", 400

    article_path = f"{getcwd()}/articles/{category}/{article_name}.html"
    print(article_path)

    if not path.exists(article_path):
        return "Article not found", 404

    with open(article_path, 'r', encoding='utf-8') as file:
        content = file.read()

    return render_template("article.html", content=content, category=category, article=article_name)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/members")
def members():
    return render_template("members.html")

@app.route("/journal")
def journal():
    return render_template("journal.html")

@app.route("/resources")
def resources():
    return render_template("resources.html")

@app.route("/frontchain")
def frontchain():
    return render_template("frontchain.html")

if __name__ == "__main__":
    app.run(debug=True)