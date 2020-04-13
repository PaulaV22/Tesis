from flask import Flask, url_for, request, render_template, redirect
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
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = uc.getUser(email, password)
        if not user is None:
            user['logged'] = True
            uc.saveUser(user)
            return redirect(url_for('compare', id=email))

        else:
            message = "Invalid username or password"
            return render_template("login.html", email=email, password=password, msg=message)
    return render_template("login.html", email=email, password=password, msg=message)


@app.route('/compare/<id>', methods=['GET', 'POST'])
def compare(id):
    user = uc.getUserByEmail(id)
    dbs = cc.getDatabases(id)
    if id is None or not user['logged']:
        return render_template("login.html", email="", password="", msg="Plese enter a valid user")
    else:
        if request.method == 'POST':
            sequence = request.form['sequence']
            database = request.form['selectDbs']
            print(sequence)
            if (len(sequence) > 0):
                numResults = request.form['numResults']
                try:
                    results = cc.compare(sequence, numResults, database, id, True)
                    return render_template("compare.html", results=results, num=int(numResults), databases=dbs,
                                           msg="", sequence=sequence, username=user['name'], userid=id)
                except Exception as e:
                    print(e)

        return render_template("compare.html", results="", sequenceExample=sequenceExample, num=0, databases=dbs,
                           msg="", sequence="",username=user['name'], userid=id)


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
        #uc.addDbToUser(id,dbName)
        cc.createDb(id,dbName)
    return render_template("addDb.html",userid = id, msg=message)


@app.route('/inspect/<id>', methods=['GET', 'POST'])
def inspect(id):
    user = uc.getUserByEmail(id)
    if id is None or not user['logged']:
        return render_template("login.html", email="", password="",username=user['name'], msg="Plese enter a valid user")
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
    return render_template("inspect.html",userid = id,username=user['name'], msg=message,results=databases)

@app.route('/deleteDatabase', methods=['POST'])
def deleteDatabase():
    id = request.form['id']
    name =  request.form['name']
    user = uc.getUserByEmail(id)
    if id is None or not user['logged']:
        return
    else:
        cc.deleteDatabase(id,name)
        databases = cc.getDatabases(id)
        print(databases)
        return databases

@app.route('/deleteSequence', methods=['POST'])
def deleteSequence():
    id = request.form['id']
    db = request.form['dbName']
    sequenceName =  request.form['sequenceName']
    user = uc.getUserByEmail(id)
    if id is None or not user['logged']:
        return
    else:
        print( id+" "+ " "+ db +" "+ sequenceName)
        print("LLEGO A DELETE SEQ")
        cc.deleteSequence(id, db, sequenceName)
        databases = cc.getDatabases(id)
        return databases

@app.route('/addSequence', methods=['POST'])
def addSequence():
    id = request.form['id']
    user = uc.getUserByEmail(id)
    if id is None or not user['logged']:
        return
    else:
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
def align(id):
    user = uc.getUserByEmail(id)
    dbs = cc.getDatabases(id)
    if id is None or not user['logged']:
        return render_template("login.html", email="", password="",username=user['name'], msg="Plese enter a valid user")
    else:
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
                                           databases=dbs, msg="", sequence="", username=user['name'], userid=id)

                except Exception as e:
                    print(e)

        return render_template("align.html", results="", sequence1="", sequence2="", sequenceExample1= sequenceExample, sequenceExample2= sequenceExample2, num=0, databases=dbs,
                           msg="", sequence="",username=user['name'], userid=id)


@app.route('/logout/<id>', methods=['GET', 'POST'])
def logout(id):
    user = uc.getUserByEmail(id)
    if not user is None:
        user['logged'] = False
        uc.saveUser(user)
    return redirect('/')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    email = id
    message = ""
    user = uc.getUserByEmail(id)
    if (user):
        name = user['name']
        password = user['password']
        if request.method == 'POST':
            name = request.form['name']
            password = request.form['password']
            user['name'] = name
            user['password'] = password
            user['logged'] = True
            try:
                uc.saveUser(user)
                message = "Changes successfully saved"
            except Exception as e:
                print(e)
                message = e
        return render_template("editprofile.html", userid=id, msg=message, username=name, email=email, password=password)
    else:
        return render_template("login.html", email="", password="", username="", msg="Plese enter a valid user")


if __name__ == '__main__':
    app.run()