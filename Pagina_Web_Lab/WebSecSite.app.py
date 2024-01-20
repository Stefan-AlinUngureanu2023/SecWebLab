# import the Flask class from the flask module
import os

from flask import Flask, render_template, redirect, request, flash, session
import sqlite3 as sql
import logging

from werkzeug.utils import secure_filename


# create the application object
app = Flask(__name__)

# app.secret_key = "It has to be unless I don't need to log the user out"

upload_photos = 'upload\\photos'

allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
# app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['UPLOAD_PHOTOS'] = upload_photos


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


# working trivial logger
logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# End of the logger


# # use decorators to link the function to an url
# @app.route('/')
# def home():
#     return render_template('home.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# # Route for handling the login page logic
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('login.html', error=error)


@app.route('/register')
def register():
    return render_template('register.html')


# Tabel baza de date

conn = sql.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE if not exists users_Database (username TEXT, email TEXT, password TEXT, confirm_password TEXT, nume TEXT, prenume TEXT, alias TEXT, url_site TEXT)')
print("Table created successfully")
conn.close()


@app.route('/addRecord', methods=['POST', 'GET'])
def addRecord():
    if request.method == 'POST':
        try:
            msg = ""
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            nume = request.form['nume']
            prenume = request.form['prenume']
            alias = request.form['alias']
            url_site = request.form['url_site']

            if password != confirm_password:
                msg = "Password not matching"
            else:
                with sql.connect("database.db") as con:
                    cur = con.cursor()

                    cur.execute("INSERT INTO users_Database (username,email,password,confirm_password,nume,prenume,alias,url_site) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                            (username, email, password, confirm_password, nume, prenume, alias, url_site))

                    con.commit()
                    msg = "Record successfully added"

            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_PHOTOS'], filename))

        except:
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from users_Database")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


# search DB users old, but good
# ________________________________________________________________________________________________
def getusers(search):
    con = sql.connect("database.db")
    cursor = con.cursor()
#    cursor.execute("SELECT nume,prenume FROM users_Database WHERE nume LIKE ? OR prenume LIKE ?", ("%"+search+"%", "%"+search+"%"))
    cursor.execute(f"SELECT nume,prenume FROM users_Database WHERE nume LIKE '%{search}%' OR prenume LIKE '%{search}%'")
# payload ' or 1=1;-- -
    results = cursor.fetchall()
    con.close()
    return results
#
#
# @app.route("/cauta", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         data = dict(request.form)
#         users = getusers(data["search"])
#     else:
#         users = []
#
#     return render_template("cauta.html", usr=users)
# __________________________________________________________________________________________________

# Search with URL processing:

# def get_users(search_query=None):
#     db = sql.connect("database.db")
#     results = []
#     get_all_query = 'SELECT nume FROM users_Database'
#     for (comment,) in db.cursor().execute(get_all_query).fetchall():
#         if search_query is None or search_query in comment:
#             results.append(comment)
#     return results


@app.route("/search", methods=["GET", "POST"])
def search():

    search_query = request.args.get('q')

    users = getusers(search_query)

    return render_template('search.html',
                           users=users,
                           search_query=search_query)


# User login
def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username,password FROM users_Database")
    users = cur.fetchall()
    print(users)
    print("Test3284")
    con.close()
    return users


@app.route('/login', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = retrieveUsers()

        if (username, password) in users:
            print("It worked")
            return render_template('home.html', username=username)
        else:
            print("Didn't work")
            return render_template('login.html', error="Incorrect username/password")

    else:
        return render_template('login.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True)

# Metoda login SQL "SELECT * FROM users WHERE username=username AND password=password
