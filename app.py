from flask import Flask, render_template, request, jsonify
from test import App

app = Flask(__name__)

@app.route("/")
def index():
    # uri = "neo4j+s://ffceff21.databases.neo4j.io"
    # user = "neo4j"
    # password = "s3M3B0rzrxJCZtEr181zpzyzK8jkWNajVkXgcAuCebw"
    # myapp = App(uri, user, password)
    #result = myapp.create_project("Navigation App", 5)
    #myapp.find_person("Alice")
    #result = myapp.add_student_to_project("Navigation App", "Franciszek", "Cis")
    #result = myapp.find_project_team('3D Pac-Man Game')
    # myapp.close()
    # print(f"Found team for {result[0]['p']}:")
    # for row in result:
    #     #print("Created project: {p}, number of students: {n}".format(p=row['p'], n=row['n']))
    #     #print("Added {f} {l} to {p} project".format(f=row["sf"], l=row["sl"], p=row["p"]))
    #     print(f"- {row['s']}")
    return render_template('index.html')

@app.route("/createProjectForm")
def createProjectForm():
    return render_template('createProjectForm.html')

@app.route("/createProject", methods=['POST'])
def createProject():
    myapp = getApp()
    name = request.json['name'] #request.form['name']
    nr_students = request.json['nr_students'] #request.form['nr_students']
    result = myapp.create_project(name, nr_students)
    myapp.close()
    return jsonify({'name' : result[0]['p'], 'nr' : result[0]['n']})
    #return render_template('createProjectForm.html', data={'pname' : result[0]['p'], 'nr' : result[0]['n']})

@app.route("/addStudentToProjectForm")
def addStudentToProjectForm():
    return render_template('addStudentToProjectForm.html')

@app.route("/addStudentToProject", methods=['POST'])
def addStudentToProject():
    myapp = getApp()
    pname = request.form['pname']
    fname = request.form['fname']
    lname = request.form['lname']
    result = myapp.add_student_to_project(pname, fname, lname)
    myapp.close()
    return render_template('addStudentToProjectForm.html', 
                            data={'pname' : result[0]['p'], 'fname' : result[0]['sf'], 'lname' : result[0]['sl']})

@app.route("/findProjectTeamForm")
def findProjectTeamForm():
    return render_template('findProjectTeamForm.html')

@app.route("/findProjectTeam/<string:pname>", methods=['GET'])
def findProjectTeam(pname):
    myapp = getApp()
    result = myapp.find_project_team(pname)
    myapp.close()
    msg = f"W projekcie {result[0]['p']} uczestniczą: "
    for row in result:
        msg += f"- {row['s']}\n"
    return jsonify({ 'result' : msg })

@app.route("/deleteProjectForm")
def deleteProjectForm():
    return render_template('deleteProjectForm.html')

@app.route("/deleteProject/<string:pname>", methods=['DELETE'])
def deleteProject(pname):
    myapp = getApp()
    pname = request.json['pname']
    result = myapp.delete_project(pname)
    myapp.close()
    print(str(result) + "del")
    return jsonify({'deleted': pname})

def getApp():
    uri = "neo4j+s://ffceff21.databases.neo4j.io"
    user = "neo4j"
    password = "s3M3B0rzrxJCZtEr181zpzyzK8jkWNajVkXgcAuCebw"
    return App(uri, user, password)