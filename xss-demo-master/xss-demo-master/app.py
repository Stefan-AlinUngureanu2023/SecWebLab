from flask import Flask, render_template, request
import db

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
#    if request.method == 'POST':
#        db.add_comment(request.form['comment'])

    search_query = request.args.get('q')

    comments = db.get_comments(search_query)

    return render_template('index.html',
                           comments=comments,
                           search_query=search_query)

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), debug=True, port=5660)