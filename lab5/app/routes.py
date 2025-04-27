from flask import render_template, redirect, url_for, request
from app import app, db
from app.forms import URLForm
from app.models import URL
from sqlalchemy import desc

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = URLForm()
    
    if form.validate_on_submit():
        # checking if url exists
        existing_url = URL.query.filter_by(url=form.url.data).first()
        if not existing_url:
            new_url = URL(url=form.url.data)
            db.session.add(new_url)
            db.session.commit()
        return redirect(url_for('index'))
    
    # get 5 last urls sorting by upload time
    recent_urls = URL.query.order_by(desc(URL.created_at)).limit(5).all()
    return render_template('index.html', form=form, urls=recent_urls)

@app.route('/delete/<int:url_id>', methods=['POST'])
def delete_url(url_id):
    url = URL.query.get_or_404(url_id)
    db.session.delete(url)
    db.session.commit()
    return redirect(url_for('index'))