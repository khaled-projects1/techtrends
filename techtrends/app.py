import sqlite3
from flask import Flask, jsonify, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging
from logging.handlers import RotatingFileHandler


# Global variable to keep track of the number of database connections
db_connection_count = 0


# Function to configure logging
def setup_logging():
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # STDOUT handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)
    
    # File handler with rotation
    file_handler = RotatingFileHandler('techtrends.log', maxBytes=10000, backupCount=1)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)


# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global db_connection_count
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    db_connection_count += 1
    return connection


# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# Configure logging
setup_logging()


# Define the main route of the web application 
@app.route('/')
def index():
    app.logger.info('Main page accessed.')
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
        app.logger.error(f'Article with id {post_id} does not exist. Returning 404 page.')
        return render_template('404.html'), 404
    else:
        app.logger.info(f'Article "{post["title"]}" retrieved.')
        return render_template('post.html', post=post)


# Define the About Us page
@app.route('/about')
def about():
    app.logger.info('About page accessed.')
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            app.logger.info(f'New article "{title}" created.')

            return redirect(url_for('index'))

    return render_template('create.html')


# Define the health check endpoint
@app.route('/healthz', methods=['GET'])
def healthz():
    app.logger.info('Health check performed.')
    return jsonify(result="OK - healthy"), 200


# Define the metrics endpoint
@app.route('/metrics', methods=['GET'])
def metrics():
    connection = get_db_connection()
    post_count = connection.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    connection.close()
    app.logger.info('Metrics accessed.')
    return jsonify(db_connection_count=db_connection_count, post_count=post_count), 200


@app.route('/readyz', methods=['GET'])
def readiness():
    try:
        # Check if the database is reachable
        connection = get_db_connection()
        connection.execute('SELECT 1')
        connection.close()
        app.logger.info('Readiness check passed.')
        return jsonify(result="OK - ready"), 200
    except Exception as e:
        app.logger.error('Readiness check failed.')
        return jsonify(result="Error - not ready"), 500


# Start the application on port 3111
if __name__ == "__main__":
   app.run(host='0.0.0.0', port='3111')
