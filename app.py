from flask import Flask, render_template, request, jsonify
from queries import Queries

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/createProjectForm")
def createProjectForm():
    return render_template('createProjectForm.html')

@app.route("/createProject", methods=['POST'])
def createProject():
    myapp = getQueries()
    name = request.json['name']
    nr_students = request.json['nr_students']
    result = myapp.create_project(name, nr_students)
    myapp.close()
    if result:
        msg = f"Zapisano projekt o nazwie: { result[0]['p'] } i potrzebnej liczbie studentów: { result[0]['n'] }"
    else:
        msg = f"Projekt o podanej nazwie już istnieje"
    return jsonify({ 'result' : msg })
    #return render_template('createProjectForm.html', data={'pname' : result[0]['p'], 'nr' : result[0]['n']})

@app.route("/addStudentToProjectForm")
def addStudentToProjectForm():
    return render_template('addStudentToProjectForm.html')

@app.route("/addStudentToProject", methods=['POST'])
def addStudentToProject():
    myapp = getQueries()
    pname = request.json['pname']
    fname = request.json['fname']
    lname = request.json['lname']
    result = myapp.add_student_to_project(pname, fname, lname)
    myapp.close()
    if result:
        msg = f"{ result[0]['sf'] } { result[0]['sl'] } jest zapisana_y do projektu { result[0]['p'] }"
    else:
        msg = "W projekcie nie ma już więcej miejsc."
    return jsonify({ 'result' : msg })

@app.route("/findProjectTeamForm")
def findProjectTeamForm():
    return render_template('findProjectTeamForm.html')

@app.route("/findProjectTeam/<string:pname>", methods=['GET'])
def findProjectTeam(pname):
    myapp = getQueries()
    result = myapp.find_project_team(pname)
    myapp.close()
    if result:
        msg = f"W projekcie {result[0]['p']} uczestniczą (max {result[0]['pn']}): "
        for row in result:
            msg += f"- {row['s']}\n"
    else:
        msg = "W projekcie nikt nie uczestniczy lub nie ma takiego projektu"
    return jsonify({ 'result' : msg })

@app.route("/deleteProjectForm")
def deleteProjectForm():
    return render_template('deleteProjectForm.html')

@app.route("/deleteProject/<string:pname>", methods=['DELETE'])
def deleteProject(pname):
    myapp = getQueries()
    pname = request.json['pname']
    result = myapp.delete_project(pname)
    myapp.close()
    return jsonify({'result': f"Usunięto projekt {pname}"})

@app.route("/deleteStudentFromProjectForm")
def deleteStudentFromProjectForm():
    return render_template('deleteStudentFromProjectForm.html')

@app.route("/deleteStudentFromProject/<string:fname>/<string:lname>/<string:pname>", methods=['DELETE'])
def deleteStudentFromProject(fname, lname, pname):
    myapp = getQueries()
    fname = request.json['fname']
    lname = request.json['lname']
    pname = request.json['pname']
    result = myapp.delete_student_from_project(pname, fname, lname)
    myapp.close()
    return jsonify({'result': f"{fname} {lname} jest usunięta_y z projektu {pname}"})

@app.route("/updateProjectForm")
def updateProjectForm():
    return render_template('updateProjectForm.html')

@app.route("/updateProject/<string:pname>/<string:nr_students>", methods=['UPDATE'])
def updateProject(pname, nr_students):
    myapp = getQueries()
    pname = request.json['pname']
    nr_students = request.json['nr_students']
    result = myapp.update_project(pname, nr_students)
    myapp.close()
    if result:
        msg = f"Projekt { result[0]['p']} zaktualizowano: maksymalna liczba studentów wynosi { result[0]['n'] }"
    else:
        msg = "Nie istnieje taki projekt"
    return jsonify({'result': msg})
    
@app.route("/findAllProjectsForm")
def findAllProjectsForm():
    return render_template('findAllProjectsForm.html')

@app.route("/findAllProjects/", methods=['GET'])
def findAllProjects():
    myapp = getQueries()
    result = myapp.find_all_projects()
    myapp.close()
    if result:
        msg = f"Projekty: "
        for row in result:
            msg += f"- { row['p'] }, max: { row['pn'] } nl"
    else:
        msg = "Nie istnieje żaden projekt"
    return jsonify({ 'result' : msg })    

def getQueries():
    uri = "neo4j+s://ffceff21.databases.neo4j.io"
    user = "neo4j"
    password = "s3M3B0rzrxJCZtEr181zpzyzK8jkWNajVkXgcAuCebw"
    return Queries(uri, user, password)