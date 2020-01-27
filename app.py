from flask import Flask, url_for, request, render_template, redirect
from project.Controller.CompareController import CompareController as CC
from project.Controller.UserController import UserController as UC
from flask_debug import Debug
from werkzeug.utils import secure_filename
import os
import shutil

UPLOAD_FOLDER = 'project/Databases'
ALLOWED_EXTENSIONS = {'fasta','fa'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)
Debug(app)
app.run(debug=True)
cc = CC()
uc = UC()
# route and method to access to the index view.

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


sequenceExample = ">HLA030F_1\n" \
                  "GRCGTRTGTCATTTCTTCACGGGACCGAGCGGGTGCGGTTSCTGGASAGAYMCTTCTATA" \
                  "ATGGAGAAGAGWACGTGCGCTTCGACAGCGACTGGGGCGAGTWCCGGGCGGTGACCGAGC" \
                  "TRGGGCGGCCGGMCGCCGAGTACTGGAACAGCCAGAAGGASWTCCTGGAGSAGARGCGGG" \
                  "CCSAGGTGGACARGGTGTGCAGACACMACTACMGGGTCSGGGARAGKTTCWCYGKRMAAA" \
                  "MGGMWAAAAA"


@app.route('/', methods=['GET', 'POST'])
def index():
    email = ""
    password = ""
    message=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = uc.getUser(email, password)
        if not user is None:
            user['logged'] = True
            uc.saveUser(user)
            return redirect(url_for('compare', id=email))

        else:
            message = "The user is not registered"
            return render_template("login.html", email=email, password=password, msg=message)
    return render_template("login.html", email=email, password=password, msg=message)


@app.route('/compare/<id>', methods=['GET', 'POST'])
def compare(id):
    user = uc.getUserByEmail(id)
    if id is None or not user['logged']:
        return render_template("login.html", email="", password="", msg="Plese enter a valid user")

    else:
        if request.method == 'POST':
            sequence = request.form['sequence']
            database = request.form['database']
        # print(sequence)
            if (len(sequence) > 0):
                numResults = request.form['numResults']
                try:
                    results = cc.compare(sequence, numResults, database, id)
                    return render_template("compare.html", results=results, num=int(numResults), databases=user['dbs'],
                                       numDatabases=len(user['dbs']), msg="", sequence=sequence, username=user['name'],
                                        userid=id)

                except Exception as e:
                    print(e)

        return render_template("compare.html", results="", sequenceExample=sequenceExample, num=0, databases=user['dbs'],
                           numDatabases=len(user['dbs']), msg="", sequence="",username=user['name'], userid=id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    name = ""
    password = ""
    email = ""
    message = ""
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        try:
            uc.addUser(name, email, password)
            message = "The user was registered successfully"
        except Exception as e:
            print(e)
            message = e
        return render_template("register.html", msg=message, name=name, email=email, password=password)

    return render_template("register.html", msg=message, name=name, email=email, password=password)

@app.route('/addDatabase/<id>', methods=['GET', 'POST'])
def addDatabase(id):
    user = uc.getUserByEmail(id)
    if id is None or not user['logged']:
        return render_template("login.html", email="", password="", msg="Plese enter a valid user")
    message=""
    if request.method == 'POST':
        # check if the post request has the file part
        uploaded_files =  request.files.getlist("file[]")
        dbName = request.form["dbname"]
        newDb = UPLOAD_FOLDER + "/" + id + "/" + dbName
        if os.path.exists(newDb):
            shutil.rmtree(newDb)
        os.makedirs(newDb)
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename = secure_filename(file.filename)
                file.save(os.path.join(newDb,filename))
        uc.addDbToUser(id,dbName)
        cc.createDb(id,dbName)
    return render_template("addDb.html",userid = id, msg=message)


@app.route('/inspect/<id>', methods=['GET', 'POST'])
def inspect(id):
    user = uc.getUserByEmail(id)
    if id is None or not user['logged']:
        return render_template("login.html", email="", password="", msg="Plese enter a valid user")
    message = ""
    databases = cc.getDatabases(id)
    if databases is None:
        message="No databases added"

    return render_template("inspect.html",userid = id, msg=message, numResults=len(databases),results=databases)