from flask import Flask, render_template, request, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
from flask_ckeditor import CKEditor
import yaml

app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM blog")
    if resultValue > 0:
        blogs = cur.fetchall()
        cur.close()
        return render_template('index.html', blogs=blogs)
    cur.close()
    return render_template('index.html', blogs=None)

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/blogs/<int:id>/')
def blogs(id):
    cur = mysql.connection.cursor()
    resultValue = cur.execute(f"SELECT * FROM blog WHERE blog_id = {id}")
    if resultValue > 0:
        blog = cur.fetchone()
        return render_template('blog.html', blog=blog)
    return 'Blog not found'

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method != 'POST':
        return render_template('register.html')
    userDetails = request.form
    if userDetails['password'] != userDetails['confirm_password']:
        flash('Passwords do not match! Try again.', 'danger')
        return render_template('register.html')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user(first_name, last_name, username, email, password) VALUES(%s,%s,%s,%s,%s)", (userDetails['first_name'], userDetails['last_name'], userDetails['username'], userDetails['email'], userDetails['password']))

    mysql.connection.commit()
    cur.close()
    flash('Registration successful! Please login.', 'success')
    return redirect('/login')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        return render_template('login.html')
    userDetails = request.form
    username = userDetails['username']
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM user WHERE username = %s", [username])
    if resultValue > 0:
        user = cur.fetchone()
        if userDetails['password'] == user['password']:
            session['login'] = True
            session['firstName'] = user['first_name']
            session['lastName'] = user['last_name']
            flash('Welcome ' + session['firstName'] + '! You have been successfully logged in', 'success')

        else:
            cur.close()
            flash('Password does not match', 'danger')
            return render_template('login.html')
    else:
        cur.close()
        flash('User not found', 'danger')
        return render_template('login.html')
    cur.close()
    return redirect('/')

# Write a new blog
@app.route('/write-blog/',methods=['GET', 'POST'])
def write_blog():
    if request.method == 'POST':
        blogpost = request.form
        title = blogpost['title']
        body = blogpost['body']
        author = session['firstName'] + ' ' + session['lastName']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO blog(title, body, author) VALUES(%s, %s, %s)", (title, body, author))
        mysql.connection.commit()
        cur.close()
        flash("Successfully posted new blog", 'success')
        return redirect('/')
    return render_template('write_blog.html')

# View my blog
@app.route('/my-blogs/')
def view_blogs():
    author = session['firstName'] + ' ' + session['lastName']
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM blog WHERE author = %s", [author])
    if result_value <= 0:
        return render_template('my_blogs.html', my_blogs=None)
    my_blogs = cur.fetchall()
    return render_template('my_blogs.html', my_blogs=my_blogs)

# Edit blog
@app.route('/edit-blog/<int:id>/', methods=['GET', 'POST'])
def edit_blog(id):
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        title = request.form['title']
        body = request.form['body']
        cur.execute("UPDATE blog SET title = %s, body = %s where blog_id = %s", (title, body, id))

        mysql.connection.commit()
        cur.close()
        flash('Blog updated successfully', 'success')
        return redirect(f'/blogs/{id}')
    cur = mysql.connection.cursor()
    result_value = cur.execute(f"SELECT * FROM blog WHERE blog_id = {id}")
    if result_value > 0:
        blog = cur.fetchone()
        blog_form = {'title': blog['title'], 'body': blog['body']}
        return render_template('edit_blog.html', blog_form=blog_form)

@app.route('/delete-blog/<int:id>/')
def delete_blog(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM blog WHERE blog_id = {id}")
    mysql.connection.commit()
    flash("Your blog has been deleted", 'success')
    return redirect('/my-blogs')

@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
