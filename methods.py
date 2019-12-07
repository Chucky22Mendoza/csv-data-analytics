import pandas as pd
import matplotlib.pyplot as plt

def read_csv(routeFile):
    route = routeFile
    df = pd.read_csv(route)
    return df

def graph_dataframe(response, columnName, option, nameGraph):
    #print(response)
    df = response
    df = df.dropna()

    if(option == 'barra'):
        plt.hist(df[columnName])
    elif option == 'pastel':
        plt.pie(df[columnName])
    else:
        plt.plot(df[columnName])
    plt.savefig("static/img/{}.png".format(nameGraph))
    return str("{}.png".format(nameGraph))

def show_csv(file):
    df = read_csv(file)
    return df.index

