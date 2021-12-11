from flask import Flask, render_template
from test import App

app = Flask(__name__)

@app.route("/")
def index():
    uri = "neo4j+s://ffceff21.databases.neo4j.io"
    user = "neo4j"
    password = "s3M3B0rzrxJCZtEr181zpzyzK8jkWNajVkXgcAuCebw"
    app = App(uri, user, password)
    #result = app.create_project("Navigation App", 5)
    #app.find_person("Alice")
    #result = app.add_student_to_project("Navigation App", "Franciszek", "Cis")
    result = app.find_project_team('3D Pac-Man Game')
    app.close()
    print(f"Found team for {result[0]['p']}:")
    for row in result:
        #print("Created project: {p}, number of students: {n}".format(p=row['p'], n=row['n']))
        #print("Added {f} {l} to {p} project".format(f=row["sf"], l=row["sl"], p=row["p"]))
        print(f"- {row['s']}")
    return render_template('index.html')