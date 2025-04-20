from flask import Flask, render_template, request
from os import getcwd, listdir, path

app = Flask(__name__)

def get_categotries_and_articles():
    categories_path = f"{getcwd()}/articles/"
    "кортеж с именами директорий"
    categories = [(categories_name, categories_path + categories_name) for categories_name in listdir(categories_path)]
    
    data = dict()

    for category_name, category_path in categories:
        data[category_name] = [article_name[:article_name.rfind(".")] for article_name in listdir(category_path)]

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

if __name__ == "__main__":
    app.run(debug=True)