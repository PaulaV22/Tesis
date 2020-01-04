from flask import Flask, url_for, request, render_template, redirect
from project.Controller.CompareController import CompareController as CC
from flask_debug import Debug

app = Flask(__name__)
Debug(app)
app.run(debug=True)
cc = CC()

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
    #    return render_template("index.html", files=files, results=[])
    databases = cc.getDatabases()
    if request.method == 'POST':
        sequence = request.form['sequence']
        database = request.form['database']
        #print(sequence)
        if (len(sequence)>0):
            numResults = request.form['numResults']
            try:
                results = cc.compare(sequence,numResults, database)
                return render_template("index.html", results=results, num = int(numResults), databases=databases,
                                   numDatabases=len(databases), msg="", sequence=sequence)
            except Exception as e:
                print (e)
            #print(int(numResults))
            #return render_template("index.html", results="", num = 0)


    return render_template("index.html", results="", sequenceExample=sequenceExample , num=0, databases=databases,
                           numDatabases=len(databases), msg="", sequence="")



