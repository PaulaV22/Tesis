from flask import Flask, url_for, request, render_template, redirect
from project.Controller.CompareController import CompareController as CC
from project.Controller.UserController import UserController as UC
from flask_debug import Debug

app = Flask(__name__)
Debug(app)
app.run(debug=True)
cc = CC()
uc = UC()
#route and method to access to the index view.
@app.route('/',  methods=['GET', 'POST'])
def index():
    sequenceExample = ">HLA030F_1\n" \
                      "GRCGTRTGTCATTTCTTCACGGGACCGAGCGGGTGCGGTTSCTGGASAGAYMCTTCTATA" \
                      "ATGGAGAAGAGWACGTGCGCTTCGACAGCGACTGGGGCGAGTWCCGGGCGGTGACCGAGC" \
                      "TRGGGCGGCCGGMCGCCGAGTACTGGAACAGCCAGAAGGASWTCCTGGAGSAGARGCGGG" \
                      "CCSAGGTGGACARGGTGTGCAGACACMACTACMGGGTCSGGGARAGKTTCWCYGKRMAAA" \
                      "MGGMWAAAAA"
    #if request.method == 'GET':
    #    database = request.form['database']
    #    files= cc.setDb(database)
    #    return render_template("compare.html", files=files, results=[])
    databases = cc.getDatabases()
    if request.method == 'POST':
        sequence = request.form['sequence']
        database = request.form['database']
        #print(sequence)
        if (len(sequence)>0):
            numResults = request.form['numResults']
            try:
                results = cc.compare(sequence,numResults, database)
                return render_template("compare.html", results=results, num = int(numResults), databases=databases,
                                   numDatabases=len(databases), msg="", sequence=sequence)
            except Exception as e:
                print (e)
            #print(int(numResults))
            #return render_template("compare.html", results="", num = 0)


    return render_template("compare.html", results="", sequenceExample=sequenceExample , num=0, databases=databases,
                           numDatabases=len(databases), msg="", sequence="")


@app.route('/register', methods=['GET', 'POST'])
def register():
    name = ""
    password = ""
    email = ""
    message=""
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        try:
            uc.addUser(name,email,password)
            message = "The user was registered successfully"
        except Exception as e:
            print(e)
            message = e
        return render_template("register.html", msg=message, name=name, email=email, password=password)

    return render_template("register.html", msg=message, name=name , email=email, password=password)
