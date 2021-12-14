from flask import Flask, render_template, request
from test import App

app = Flask(__name__)

@app.route("/")
def index():
    uri = "neo4j+s://ffceff21.databases.neo4j.io"
    user = "neo4j"
    password = "s3M3B0rzrxJCZtEr181zpzyzK8jkWNajVkXgcAuCebw"
    myapp = App(uri, user, password)
    #result = myapp.create_project("Navigation App", 5)
    #myapp.find_person("Alice")
    #result = myapp.add_student_to_project("Navigation App", "Franciszek", "Cis")
    result = myapp.find_project_team('3D Pac-Man Game')
    myapp.close()
    print(f"Found team for {result[0]['p']}:")
    for row in result:
        #print("Created project: {p}, number of students: {n}".format(p=row['p'], n=row['n']))
        #print("Added {f} {l} to {p} project".format(f=row["sf"], l=row["sl"], p=row["p"]))
        print(f"- {row['s']}")
    return render_template('index.html')

@app.route("/createProject", methods=['POST'])
def createProject():
    uri = "neo4j+s://ffceff21.databases.neo4j.io"
    user = "neo4j"
    password = "s3M3B0rzrxJCZtEr181zpzyzK8jkWNajVkXgcAuCebw"
    myapp = App(uri, user, password)
    name = request.form['name']
    nr_students = request.form['nr_students']
    result = myapp.create_project(name, nr_students)
    myapp.close()
    return str(result)

@app.route("/save", methods=['POST'])
def save():
    fname = request.form['fname']
    return fname