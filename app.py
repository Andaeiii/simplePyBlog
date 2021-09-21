from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

from datetime import datetime


app = Flask(__name__)
# mysql url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://andaeiii:pass1234@localhost/ppr_blog'
db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)


@app.route('/')
def index():

    p = Blogpost.query.order_by(Blogpost.date_posted).all()
    return render_template('index.html', posts=p)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    p = Blogpost.query.filter_by(id=post_id).one()  # first, one..
   # date_posted = p.date_posted.strftime('%B %d, %Y')
    return render_template('post.html', post=p)  # datePosted=date_posted)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
def addpost():
    # retrieve all the form contents....
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle,
                    author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

    # return '<h1> Title: {} Subtitle: {} Author: {}  content : {} <h1>'.format(title, subtitle, author, content)


if __name__ == '__main__':
    app.run(debug=True)
