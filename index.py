from flask import Flask, render_template, url_for, request, redirect, flash
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

    return render_template("uploadFile.html", tables=[df.to_html(classes='data', header="true")], titles=df.columns.values, save_data = file)

@app.route('/message', methods=['POST'])
def message():

    column = request.form['firstColumn']
    graph = request.form['graph']
    nameGraph = request.form['nameGraph']

    if(graph != '0' and column != '0'):
        graph_dataframe(response, column, graph, nameGraph)
        flash("Graph Saved Successfully")

        return redirect(url_for('index'))
    else:
        flash("Error trying save the graph")

        return redirect(url_for('index'))

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