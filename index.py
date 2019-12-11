import os
import io
from flask import Flask, render_template, url_for, request, redirect, flash, session, escape
from flask_caching import Cache
from werkzeug.utils import secure_filename
#from methods import read_csv, graph_dataframe
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import numpy as np

app = Flask(__name__)
#SESSION_TYPE = 'filesystem'

# settings
app.config['UPLOAD_FOLDER'] = './'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'mysecretkey'

response = ''

#VISTA PRINCIPAL
@app.route('/')
def index():
    session.clear()
    return render_template("home.html")

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    #OBTENER EL ARCHIVO DEL FORMULARIO
    file = request.files['fileUpload']
    #NOMBRE DEL ARCHIVO
    filename = secure_filename(file.filename)
    #GUARDAR ARCHIVO EN CONFIGURACION DE LA VARIABLE UPLOAD FOLDER
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #VARIABLE GLOBAL QUE CONTIENE EL ARCHIVO
    global response
    response = pd.read_csv(filename)
    #global data
    #data = request.args.get("data", response)
    #MOSTRAR SOLO LOS 5 PRIMEROS DE LA TABLA
    df = response.head()

    #RENDERIZAR LA VISTA CON LA TABLA EN SUS 5 PRIMERAS FILAS
    return render_template("uploadFile.html", tables=[df.to_html(classes='data', header="true")], titles=df.columns.values)

#VISTA QUE REALIZA EL PROCESO DE GRAFICACIÓN FINALIZANDO CON UN MSG E IMG DE LA GRÁFICA
@app.route('/message', methods=['POST'])
def message():
    global plot_url  #variable global que contiene en caché la imagen
    plt.clf()  #limpiar la figuara
    ###Valores del formulario
    column = request.form['firstColumn']
    graph = request.form['graph']
    nameGraph = request.form['nameGraph']

    #data_server = escape(data)
    #df = pd.read_csv(data_server)
    #print(df)

    #Validar que los campos sean correctos
    if(graph != '0' and column != '0'):
        #img_transform = graph_dataframe(data_server, column, graph, nameGraph)
        #img_transform = graph_dataframe(response, column, graph, nameGraph)

        #path = os.path.join(app.config['UPLOAD_FOLDER'], "{}.png".format(nameGraph))
        #print(path)
        temp_df = response.iloc[0:10] #seleccionar solo los primeros 10 registros
        temp_df = temp_df.fillna(0)
        #print(temp_df)

        #Graficación por punto
        if(graph == 'punto'):
            img = io.BytesIO() #imagen a stream
            plt.title("Graph: "+graph+"   Column: "+column) #nombrar la gráfica
            plt.plot(temp_df[column], '--')  #tipo de gráfica
            #plt.savefig(path)
            plt.savefig(img, format='png')  #guardar la figura
            #plt_temp = plt
            #plt_temp.savefig("static/img/{}.png".format(nameGraph)) #guardar en servidor
            img.seek(0) #solicitar
            plot_url = base64.b64encode(img.getvalue()).decode()  #imagen guardada en url base64 en memoria caché

        #Graficación lineal
        if(graph == 'lineal'):
            img = io.BytesIO() #imagen a stream
            plt.title("Graph: "+graph+"   Column: "+column) #nombrar la gráfica
            plt.plot(temp_df[column])  #tipo de gráfica
            #plt.savefig(path)
            plt.savefig(img, format='png')  #guardar la figura
            #plt_temp = plt
            #plt_temp.savefig("static/img/{}.png".format(nameGraph)) #guardar en servidor
            img.seek(0) #solicitar
            plot_url = base64.b64encode(img.getvalue()).decode()  #imagen guardada en url base64 en memoria caché

        #Graficación por pastel
        if(graph == 'pastel'):
            img = io.BytesIO() #imagen a stream
            plt.title("Graph: "+graph+"   Column: "+column) #nombrar la gráfica
            plt.pie(temp_df[column], labels=temp_df[column], autopct="%0.1f %%")  #tipo de gráfica
            #plt.savefig(path)
            plt.savefig(img, format='png')  #guardar la figura
            #plt_temp = plt
            #plt_temp.savefig("static/img/{}.png".format(nameGraph)) #guardar en servidor
            img.seek(0) #solicitar
            plot_url = base64.b64encode(img.getvalue()).decode()  #imagen guardada en url base64 en memoria caché

        #Graficación por barra
        if(graph == 'barra'):
            img = io.BytesIO() #imagen a stream
            plt.title("Graph: "+graph+"   Column: "+column) #nombrar la gráfica
            plt.hist(temp_df[column])  #tipo de gráfica
            #plt.savefig(path)
            #plt.savefig(img, format='png')  #guardar la figura
            #plt_temp = plt
            #plt_temp.savefig("static/img/{}.png".format(nameGraph)) #guardar en servidor
            img.seek(0) #solicitar
            plot_url = base64.b64encode(img.getvalue()).decode()  #imagen guardada en url base64 en memoria caché

        #print(plot_url)
        #session.clear() #Cerrar variables de session
        flash("Graph Saved Successfully") #utilizar flash para mandar mensajes entre vistas

        return render_template("show_img.html", url_img = plot_url) #renderizado de la vista con la imagen cargada de la graficación
    else:
        flash("Error trying save the graph") #utilizar flash para mandar mensajes entre vistas
        return render_template("show_img.html")

#ERROR 404
@app.errorhandler(404)
def page_not_found(error):
    msg = "Error 404. Page not found"
    return render_template('message.html', message=msg)

#CANCELAR OPERACION
@app.route('/cancel_message')
def cancel_message():
    flash('Operation canceled')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=4000, debug=True)
