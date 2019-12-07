from flask import Flask, render_template, url_for, request, redirect, flash
from flask_caching import Cache
from methods import read_csv, graph_dataframe

file = ""

app = Flask(__name__)

# settings
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    file = request.files['fileUpload']
    global response
    response = read_csv(file)
    df = response.head()

    return render_template("uploadFile.html", tables=[df.to_html(classes='data', header="true")], titles=df.columns.values)

@app.route('/message', methods=['POST'])
def message():

    column = request.form['firstColumn']
    graph = request.form['graph']
    nameGraph = request.form['nameGraph']

    if(graph != '0' and column != '0'):
        img_transform = graph_dataframe(response, column, graph, nameGraph)
        flash("Graph Saved Successfully")

        return render_template("show_img.html", url_img = img_transform)
    else:
        flash("Error trying save the graph")
        return render_template("show_img.html")

@app.errorhandler(404)
def page_not_found(error):
    msg = "Error 404. Page not found"
    return render_template('message.html', message=msg)

@app.route('/cancel_message')
def cancel_message():
    flash('Operation canceled')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=4000, debug=True)