from flask import Flask, request, render_template
import sqlite3

def startup():

    try:
        dbname = input("Name of the database you will use")
        check_connection = 'file:{}.db?mode=rw'.format(dbname)
        conn = sqlite3.connect(check_connection, uri=True)
        database_name = "./{}.db".format(dbname)
        print(database_name)
        if __name__ == '__main__':
            app.run(debug=True)
    except sqlite3.OperationalError:
        #If database DNE print out error
        print("database doesn't exist")
        exit(0)


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/query3')
def query3():
    return render_template('query3.html')

@app.route('/result')
def result():
    djf = 362457
    return render_template('result.html', output = djf)

startup()
