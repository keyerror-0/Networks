from app import app 
from app.src.parse_engine import Parser
from app.models import Category
from flask import render_template, jsonify


@app.route('/')
def index():
    with Parser() as parser:
        return render_template('index.html', title = 'parse_riceweare', categories = parser.get_available_categories())

@app.route('/parse/<string:category>')
def parse(category):

    # Проверяем есть ли уже данные в базе для этой категории
    existing_category = Category.query.filter_by(name=category).first()
    
    if existing_category and existing_category.items:
        # Если категория существует и есть товары - возвращаем из БД
        print(f"Данные категории {category} уже существуют в базе, используем кеш")
        return render_template('parse.html', items=Parser.get_items_by_category(category), category = category)
    
    # Если данных нет - выполняем парсинг
    with Parser() as parser:
        print(f"Парсим категорию {category}...")
        result = parser.parse_category(category)
    
    # Всегда возвращаем данные из БД после парсинга
    items = Parser.get_items_by_category(category)
    return jsonify(items)
