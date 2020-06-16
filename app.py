from flask import Flask, url_for, request, render_template, redirect
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user,logout_user
from werkzeug.urls import url_parse
from project.Controller.CompareController import CompareController as CC
from project.Controller.UserController import UserController as UC
#from flask_debug import Debug
from werkzeug.utils import secure_filename
import os
import shutil
import json

UPLOAD_FOLDER = 'project/Databases'
ALLOWED_EXTENSIONS = {'fasta','fa'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] ='7\xa5\xeb\xe52\xa8@]\x02 |/\xc7\xbal\x83'

login_manager = LoginManager(app)
#login_manager.session_protection = "strong"
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

sequenceExample2 = ">HLA030F_2\n" \
                  "GRCGRRTGTCATTTCTTCACGGGACCGAGCGGGTGCGGTTSCTGGASAGAYMCTTCTATA" \
                  "ATGGAGAAGAGWACGTGCGCTTCGACAGCGACTGGGGCGAGTWCCGGGCGGTGACCGAGC" \
                  "TRGGGCGGCCGGMCGCCGAGTACTGGAACAGCCAGAAGGASWTCCTGGAGSAGARGCGGG" \
                  "CCSAGGTGGACARGGTGTGCAGACACMACTACMGGGTCSGGGARAGKTTCWCYGKRMAAA" \
                  "MGGMWAAAAT"



@app.route('/', methods=['GET', 'POST'])
def index():
    email = ""
    password = ""
    message=""
    if current_user.is_authenticated:
        return redirect(url_for('compare', id=current_user.get_id()))
    if request.method == 'POST':
        user = uc.getUser(request.form['email'])
        if user is not None:
            if user.check_password(request.form['password']):
                login_user(user)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('compare', id=user.get_id())
                return redirect(next_page)
    return render_template("login.html", email=email, password=password, msg=message)

@login_manager.unauthorized_handler
def unauthorized():
    email = ""
    password = ""
    message = "UNAUTHORIZED: Invalid username or password"

    return render_template("login.html", email=email, password=password, msg=message)
    # do stuff

@app.route('/compare/<id>', methods=['GET', 'POST'])
@login_required
def compare(id):
    print("IN COMPARE")
    user = uc.getUser(id)
    dbs = cc.getDatabases(id)
    if request.method == 'POST':
        sequence = request.form['sequence']
        database = request.form['selectDbs']
        print(sequence)
        if (len(sequence) > 0):
            numResults = request.form['numResults']
            try:
                results = cc.compare(sequence, numResults, database, id, True)
                return render_template("compare.html", results=results, num=int(numResults), databases=dbs,
                                       msg="", sequence=sequence, username=user.name, userid=id)
            except Exception as e:
                print(e)

    return render_template("compare.html", results="", sequenceExample=sequenceExample, num=0, databases=dbs,
                       msg="", sequence="",username=user.name, userid=id)


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
@login_required
def addDatabase(id):
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
        #uc.addDbToUser(id,dbName)
        cc.createDb(id,dbName)
    return render_template("addDb.html",userid = id, msg=message)


@app.route('/inspect/<id>', methods=['GET', 'POST'])
@login_required
def inspect(id):
    user = uc.getUser(id)
    message = ""
    if request.method == 'POST':
        # check if the post request has the file part
        uploaded_files =  request.files.getlist("dbfile[]")
        print(request.files.getlist("dbfile[]"))
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
        #uc.addDbToUser(id,dbName)
        cc.createDb(id,dbName)
    databases = cc.getDatabases(id)
    if databases is None:
        message="No databases added"
    return render_template("inspect.html",userid = id,username=user.name, msg=message,results=databases)

@app.route('/deleteDatabase', methods=['POST'])
@login_required
def deleteDatabase():
    id = request.form['id']
    name =  request.form['name']
    cc.deleteDatabase(id,name)
    databases = cc.getDatabases(id)
    return databases

@app.route('/deleteSequence', methods=['POST'])
@login_required
def deleteSequence():
    id = request.form['id']
    db = request.form['dbName']
    sequenceName =  request.form['sequenceName']
    cc.deleteSequence(id, db, sequenceName)
    databases = cc.getDatabases(id)
    return databases

@app.route('/addSequence', methods=['POST'])
@login_required
def addSequence():
    id = request.form['id']
    uploaded_file = request.files.get('file')
    dbName = request.form["dbName"]
    newFilePath = UPLOAD_FOLDER + "/" + id + "/" + dbName
    if os.path.exists(newFilePath):
                    # Check if the file is one of the allowed types/extensions
        if uploaded_file and allowed_file(uploaded_file.filename):
                # Make the filename safe, remove unsupported chars
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(newFilePath, filename))
    cc.restartDb(id, dbName)
    databases = cc.getDatabases(id)
    return databases




@app.route('/align/<id>', methods=['GET', 'POST'])
@login_required
def align(id):
    user = uc.getUserByEmail(id)
    dbs = cc.getDatabases(id)
    if request.method == 'POST':
        sequence1 = request.form['sequence1']
        sequence2 = request.form['sequence2']
        if ((len(sequence1) > 0) and (len(sequence2) >0)):
            seq1Name = sequence1.partition('\n')[0]
            seq1Name = ''.join(e for e in seq1Name if e.isalnum())
            seq1Name = seq1Name+".fa"
            dbName ="align"
            newDb = UPLOAD_FOLDER + "/" + id + "/" +dbName
            if os.path.exists(newDb):
                shutil.rmtree(newDb)
            os.makedirs(newDb)
            seq1Path = UPLOAD_FOLDER + "/" + id + "/"+dbName+"/"+seq1Name
            file = open(seq1Path, 'w+')
            file.write(sequence1)
            file.close()
            try:
                cc.createSimpleDb(id, "align")
                print("simple db created app.py. to see results")
                results = cc.compare(sequence2, 1, dbName, id, False)
                print(results)
                cc.deleteDatabase(id,dbName)
                #print("app.py Temporal align db deleted")
                return render_template("align.html", results=results, sequence1=sequence1, sequence2=sequence2,
                                       sequenceExample1=sequenceExample, sequenceExample2=sequenceExample2,  num=0,
                                       databases=dbs, msg="", sequence="", username=user.name, userid=id)

            except Exception as e:
                print(e)

    return render_template("align.html", results="", sequence1="", sequence2="", sequenceExample1= sequenceExample, sequenceExample2= sequenceExample2, num=0, databases=dbs,
                           msg="", sequence="",username=user.name, userid=id)


@app.route('/logout/<id>', methods=['GET', 'POST'])
@login_required
def logout(id):
    logout_user()
    return redirect('/')

@app.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    email = id
    message = ""
    user = uc.getUserByEmail(id)
    if (user):
        name = user.name
        password = user.password
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            user.name = name
            user.password = password
            try:
                uc.saveUser(user)
                message = "Changes successfully saved"
            except Exception as e:
                print(e)
                message = e
        return render_template("editprofile.html", userid=id, msg=message, username=name, email=email, password=password)
    else:
        return render_template("login.html", email="", password="", username="", msg="Plese enter a valid user")

@login_manager.user_loader
def load_user(user_id):
    return uc.getUser(user_id)

if __name__ == '__main__':
    app.run()