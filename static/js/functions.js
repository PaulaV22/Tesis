var dbs= [];
var columns1 = [{title: "SCORE", dataKey: "SCORE"}, {title: "EVALUE", dataKey: "EVALUE"},{title: "SIMILARITY", dataKey: "SIMILARITY"},]
var rows1 = [];
var columns2 = [
            {title: "Name", dataKey: "Name"},
            {title: "Start", dataKey: "Start"},
            {title: "Alignment", dataKey: "Alignment"},
            {title: "End", dataKey: "End"},

        ];
var rows2 = [];

function showLoading(){
    //var seq = document.getElementById("sequence").value;
    document.getElementById("loader").removeAttribute("hidden");
    //createTable();
}

function showMsg(){
    msg = document.getElementById("msg").value;
    if (msg!=""){
        alert(msg);
    }
}

function createTable(){
    var table = document.createElement("table");
    table.setAttribute("id", "table_results");
    table.setAttribute("class", "table table-striped table-dark");
    var cantResults = document.getElementById("numResults").value;
    var results=document.getElementById("results-input").value;
    console.log(results);
    if (results.length!=0){
        results = JSON.parse(results);
        var thead = document.createElement("thead");
        var cols = ["Sequences", "Blast score", "Blast e-value", "Similarity"];
        var atts = ['id', 'score', 'evalue', 'similarity']
        var tr = thead.insertRow(-1);
        for (var c in cols) {
            var th = document.createElement("th");
            th.innerHTML = cols[c];
            tr.appendChild(th);
        }
        thead.appendChild(tr);
        table.appendChild(thead);

        var tbody = document.createElement("tbody");
        for (var i = 0; i < results.length ; i++) {
            var item = results[i]
            tr = tbody.insertRow(-1);
            for(var j in atts){
                var tabCell = tr.insertCell(-1);
                tabCell.innerHTML = item[atts[j]];
            }
        }
        table.appendChild(tbody);

        var divContainer = document.getElementById("table-results");
        divContainer.innerHTML = "";
        divContainer.appendChild(table);
        divContainer.removeAttribute("hidden");
    }
}

function showMessage(){
    msg = document.getElementById("msg").value;
    console.log(msg);

    label = document.getElementById("lblmessage");
    label.innerHTML = msg;
    var divContainer = document.getElementById("message");
    divContainer.removeAttribute("hidden");
}

function w3_open() {
  document.getElementById("mySidebar").style.display = "block";
  document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
  document.getElementById("mySidebar").style.display = "none";
  document.getElementById("myOverlay").style.display = "none";
}


jQuery(function ($) {

    $(".sidebar-dropdown > a").click(function() {
  $(".sidebar-submenu").slideUp(200);
  if (
    $(this)
      .parent()
      .hasClass("active")
  ) {
    $(".sidebar-dropdown").removeClass("active");
    $(this)
      .parent()
      .removeClass("active");
  } else {
    $(".sidebar-dropdown").removeClass("active");
    $(this)
      .next(".sidebar-submenu")
      .slideDown(200);
    $(this)
      .parent()
      .addClass("active");
  }
});


});

function configureSideBar(){
  /*  var username = document.getElementById("username").value;
    console.log(username);
    var span = document.getElementById("usernameSpan");
    span.innerHTML = username; */
}

function createSelectOption(){
   var select = document.getElementById("database");
   var results=document.getElementById("results-input").value;
   if (results.length!=0){
        results = JSON.parse(results);
        for (var i = 0; i < results.length(); i++){
            var db = results[i]
            var option=document.createElement("option");
            option.setAttribute("value",db["Name"]);
            option.setAttribute("label",db["Name"]);
            // Añadimos el option al select
            select.appendChild(option);
        }
   }
}

function createDatabasesTable(){
    var table = document.createElement("table");
    table.setAttribute("id", "table_results");
    table.setAttribute("class", "table table-striped table-dark");
    var results=document.getElementById("results-input").value;
    if ((results.length!=0)&& (results!="None")){
        results = JSON.parse(results);
        dbs = results;
        var thead = document.createElement("thead");
        var cols = ["Name", "Files", "Expand"];
        var tr = thead.insertRow(-1);
            var th1 = document.createElement("th");
            th1.innerHTML = "NAME";
            tr.appendChild(th1);

             var th2 = document.createElement("th");
            th2.innerHTML = "FILES";
            tr.appendChild(th2);

             var th3 = document.createElement("th");
            th3.innerHTML = "DELETE";
            tr.appendChild(th3);

             var th4 = document.createElement("th");
            th4.innerHTML = "ADD SEQUENCE";
            tr.appendChild(th4);

             var th5 = document.createElement("th");
            th5.innerHTML = "EXPAND";
            tr.appendChild(th5);


        thead.appendChild(tr);
        table.appendChild(thead);

        var tbody = document.createElement("tbody");
        for (var i = 0; i < results.length ; i++) {
            var item = results[i]
            tr.className= "accordion-toggle collapsed";
            tr.setAttribute("data-toggle", "collapse");
            var collapseId = "collapse"+i;
            tr.setAttribute("href","#"+collapseId );

            tr = tbody.insertRow(-1);


            var tabCell1 = tr.insertCell(-1);
            tabCell1.innerHTML = item["Name"];
            var tabCell2 = tr.insertCell(-1);
            tabCell2.innerHTML = item["Files"];

            var buttonDelete = document.createElement("button");
            buttonDelete.setAttribute("type", "button");
            buttonDelete.className="button-icon";
            buttonDelete.setAttribute("id", "delete_"+i);
            buttonDelete.innerHTML = '<i class = "fa fa-trash-o"></i>';
             buttonDelete.addEventListener('click', function(){
                    var db = this.id.split('_')[1];
                    var name = dbs[db]["Name"];
                    showModalDeleteDatabase(name, db);
               });

            var tabCell3 = tr.insertCell(-1);
            //tabCell.appendChild(link);
            tabCell3.appendChild(buttonDelete);

            var buttonAdd = document.createElement("button");
            buttonAdd.setAttribute("type", "button");
            buttonAdd.className="button-icon";
            buttonAdd.setAttribute("id", "add_"+i);
            buttonAdd.innerHTML = '<i class = "fa fa-plus"></i>';
            buttonAdd.addEventListener('click', function(){
                   var input = document.getElementById("btnFile");
                   var clicked = this;
                   input.onchange = function(e) {
                        console.log(input.files);
                        console.log(clicked);
                        if (input.files.length>0){
                            showUploadModal(input.files, clicked.id)
                        }
                    };
                   $('#btnFile').trigger('click');

               });

            var tabCell4 = tr.insertCell(-1);
            //tabCell.appendChild(link);
            tabCell4.appendChild(buttonAdd);

            var accordionId = "accordion"+i

            var button = document.createElement("button");
            button.setAttribute("type", "button");
            button.className="button-icon";
            button.setAttribute("data-toggle","collapse");
            button.setAttribute("data-target", "#"+accordionId);
            button.innerHTML = '<i class = "fa  fa-angle-down"></i>';

            var tabCell5 = tr.insertCell(-1);
            //tabCell.appendChild(link);
            tabCell5.appendChild(button);


            var hiddenTr = tbody.insertRow(-1);
            hiddenTr.className="table-padding";
            hiddenTr.setAttribute("id", accordionId);
            hiddenTr.setAttribute("class", "collapse");

            var tabCellName = hiddenTr.insertCell(-1);
            var fileList = item["FileList"];
            tabCellName.setAttribute("colspan", 5)




            //hidden row header
            var divHeaderRow = document.createElement("div");
            var divHeaderSubRow = document.createElement("div");
            divHeaderSubRow.className="flex-row";
            var divHeaderSubRow1 = document.createElement("div");
            divHeaderSubRow1.className="col-md-5 text-left";
            divHeaderSubRow1.innerHTML = "SEQUENCE NAME";
            var divHeaderSubRow2 = document.createElement("div");
            divHeaderSubRow2.className="col-md-2 text-left";
            divHeaderSubRow2.innerHTML= "SIZE"
            var divHeaderSubRow3 = document.createElement("div");
            divHeaderSubRow3.className="col-md-2";
            divHeaderSubRow3.innerHTML="INSPECT"
            var divHeaderSubRow4 = document.createElement("div");
            divHeaderSubRow4.className="col-md-3";
            divHeaderSubRow4.innerHTML= "DELETE SEQUENCE"

            divHeaderSubRow.appendChild(divHeaderSubRow1);
            divHeaderSubRow.appendChild(divHeaderSubRow2);
            divHeaderSubRow.appendChild(divHeaderSubRow3);
            divHeaderSubRow.appendChild(divHeaderSubRow4);

            divHeaderRow.appendChild(divHeaderSubRow);

            tabCellName.appendChild(divHeaderRow);

            for (var k= 0; k < fileList.length; k++) {
               var fileInfo = fileList[k]
               var divRow = document.createElement("div");
               var divSubRow = document.createElement("div");
               divSubRow.className="flex-row";
               var divSubRow1 = document.createElement("div");
               divSubRow1.className="col-md-5 text-left";
               divSubRow1.innerHTML = fileInfo["name"];
               var divSubRow2 = document.createElement("div");
               divSubRow2.className="col-md-2  text-left";
               divSubRow2.innerHTML= fileInfo["size"];
                var divSubRow3 = document.createElement("div");
               divSubRow3.className="col-md-2";

                var buttonInspect = document.createElement("button");
                buttonInspect.setAttribute("type", "button");
                buttonInspect.className="button-icon";
                buttonInspect.setAttribute("id", i+"_"+k);
                buttonInspect.innerHTML = '<i class = "fa  fa-search"></i>';
                buttonInspect.addEventListener('click', function(){
                    var db = this.id.split('_')[0];
                    var file = this.id.split('_')[1];
                    var content = dbs[db]["FileList"][file]["content"];
                    var name = dbs[db]["FileList"][file]["name"];
                    showModal(name, content);
               });
                divSubRow3.appendChild(buttonInspect);


                var divSubRow4 = document.createElement("div");
                divSubRow4.className="col-md-3";

                var buttonDelete = document.createElement("button");
                buttonDelete.setAttribute("type", "button");
                buttonDelete.className="button-icon";
                buttonDelete.setAttribute("id", i+"_"+k+"_delete");
                buttonDelete.innerHTML = '<i class = "fa  fa-trash-o"></i>';
                buttonDelete.addEventListener('click', function(){
                    var db = this.id.split('_')[0];
                    var file = this.id.split('_')[1];
                    var name = dbs[db]["FileList"][file]["name"];
                    showModalDeleteSequence(db, name);
               });
               divSubRow4.appendChild(buttonDelete);

               divSubRow.appendChild(divSubRow1);
               divSubRow.appendChild(divSubRow2);
               divSubRow.appendChild(divSubRow3);
               divSubRow.appendChild(divSubRow4);

               divRow.appendChild(divSubRow);
               tabCellName.appendChild(divRow);
            }
            hiddenTr.appendChild(tabCellName);
            //link.onClick = toggleRow(i);


        }
        table.appendChild(tbody);

        var divContainer = document.getElementById("table-results");
        divContainer.innerHTML = "";
        divContainer.appendChild(table);
        divContainer.removeAttribute("hidden");
    }
}

function toggleRow(id){
    var row = document.getElementById(id);
    if (row){
        row.removeAttribute("hidden");
    }
}

function showModal(name, content){
    var modal = document.getElementById("modalSequences");
    var title = document.getElementById("modalSequences-title");
    var body = document.getElementById("modalSequences-body");

    title.innerHTML = name;
    body.innerHTML = content;
    $('#modalSequences').modal('show');

         // initializes and invokes show immediately
}

var deleteDatabase = function(){
     document.getElementById("loader").removeAttribute("hidden");
     var db =  document.getElementById("dbToDelete").value;
     var userid =  document.getElementById("userid").value;
     var dbName = dbs[db]["Name"];
     $.post('/deleteDatabase', {
                id: userid,
                name: dbName,
            }).done(function(response) {
                document.getElementById("loader").setAttribute("hidden", true);
                document.getElementById("results-input").value = response;
                createDatabasesTable();
            }).fail(function() {
                document.getElementById("loader").setAttribute("hidden", true);
                console.log("error deleting db ");
            });
}

function showModalDeleteDatabase(name, db){
    var modal = document.getElementById("modalDeleteDb");
    var title = document.getElementById("modalDelete-title");
    var body = document.getElementById("modalDelete-body");
    document.getElementById( "buttonDelete" ).setAttribute( "onClick", "javascript: deleteDatabase();" );

    var saveDb =  document.getElementById("dbToDelete");
    saveDb.value = db;
    title.innerHTML = "Delete Database ";
    body.innerHTML = "Confirm delete database "+ name +" ?";
    $('#modalDeleteDb').modal('show');
}

var deleteSequence = function(){
     document.getElementById("loader").removeAttribute("hidden");
     var sequence =  document.getElementById("sequenceToDelete").value;
     var db = document.getElementById("dbToDelete").value;
     var userid =  document.getElementById("userid").value;
     var dbName = dbs[db]["Name"];
      $.post('/deleteSequence', {
                id: userid,
                dbName: dbName,
                sequenceName: sequence
            }).done(function(response) {
                document.getElementById("loader").setAttribute("hidden", true);
                document.getElementById("results-input").value = response;
                createDatabasesTable();
            }).fail(function() {
                document.getElementById("loader").setAttribute("hidden", true);
                console.log("error deleting db ");
            });
}

function showModalDeleteSequence(db, name){
   var modal = document.getElementById("modalDeleteDb");
    var title = document.getElementById("modalDelete-title");
    var body = document.getElementById("modalDelete-body");
    var userid =  document.getElementById("userid").value;
    document.getElementById( "buttonDelete" ).setAttribute( "onClick", "javascript: deleteSequence();" );
    var saveDb =  document.getElementById("dbToDelete");
    saveDb.value = db;
    var saveSeq=  document.getElementById("sequenceToDelete");
    saveSeq.value = name;
    title.innerHTML = "Delete Sequence ";
    body.innerHTML = "Confirm delete sequence "+ name +" from database ?";
    $('#modalDeleteDb').modal('show');
}



var addSequence = function(){
     document.getElementById("loader").removeAttribute("hidden");
     var sequence =  document.getElementById("sequenceToDelete").value;
     var dbName = document.getElementById("dbToAddSeq").value;
     var input = document.getElementById("btnFile");
     var userid =  document.getElementById("userid").value;

     var file = input.files[0];
     var formData = new FormData();
     formData.append('file', file);
     formData.append('id', userid);
     formData.append('dbName', dbName);

     $.ajax({
            type: 'POST',
            url: '/addSequence',
            data: formData,
            contentType: false,
            cache: false,
            processData:false,
            success: function(response){ //console.log(response);
                document.getElementById("loader").setAttribute("hidden", true);
                document.getElementById("results-input").value = response;
                createDatabasesTable();
            },
            fail: function(){
                document.getElementById("loader").setAttribute("hidden", true);
                console.log("error agregando secuencia");
            }
        });

}

function showUploadModal(fileList, addId){
    var dbIndex = addId.split('_')[1];
    var db = dbs[dbIndex];
    console.log(db);
    var modal = document.getElementById("modalDeleteDb");
    var title = document.getElementById("modalDelete-title");
    var body = document.getElementById("modalDelete-body");
    var userid =  document.getElementById("userid").value;
    document.getElementById( "buttonDelete" ).setAttribute( "onClick", "javascript: addSequence();" );
    var saveDb =  document.getElementById("dbToAddSeq");
    saveDb.value = db["Name"];
    var saveSeq=  document.getElementById("newSeqName");
    saveSeq.value = fileList[0].name;
    console.log(fileList[0].name);
    title.innerHTML = "Add Sequence ";
    body.innerHTML = "Confirm adding sequence "+ fileList[0].name +" to the database "+db["Name"]+"?";
    $('#modalDeleteDb').modal('show');
}



function setDatabases(){
    var dbs = document.getElementById("databases").value;
    if(dbs!="None"){
     dbs = JSON.parse(dbs);
    var select = document.getElementById("selectDbs");
    for (var k= 0; k < dbs.length; k++) {
        var opt = document.createElement('option');
        opt.value = dbs[k]["Name"];
        opt.innerHTML = dbs[k]["Name"];
        select.appendChild(opt);
        }
    }
}

function openSideBar(){
    var div = document.getElementById("sidebar");
    div.classList.add("displayed");
    var div2 = document.getElementById("left-panel");
    div2.classList.add("toggled");
    var button = document.getElementById("close-sidebar");
    button.setAttribute("hidden", "true");
}

function getContent(sequence){
    arr = sequence.split("\n");
    name = arr[0];
    name = name.split(" ")[0];
    arr.splice(0,1);
    content = arr.join('');
    return content;
}

function getAlignment(seq1, seq2, seq1start, seq2start){
    var output = "";
}

function min (val1,val2){
    if (val1>=val2) return val2;
    return val1;
}

function max(val1,val2){
    if (val1>=val2) return val1;
    return val2;
}

function showResults_(){
   var results=document.getElementById("results-input").value;
   var divResults = document.getElementById("table-results");
    if (results.length>0){
        results = JSON.parse(results);
        console.log(results)
        var alignment = results[results.length-1]

        var score =  alignment.score;
        var evalue = alignment.evalue;
        var similarity = alignment.similarity;

        //var txtContent = "";
        var firstRow = document.createElement("div");
        firstRow.setAttribute("class","flex-row separated");
        var c1 = document.createElement("div");
        c1.setAttribute("class","col-md-4");
        c1.innerHTML = "<b>SCORE: </b>"+score;
        var c2 = document.createElement("div");
        c2.setAttribute("class","col-md-4");
        c2.innerHTML = "<b>E-VALUE: </b>"+ evalue;
        var c3 = document.createElement("div");
        c3.setAttribute("class","col-md-4");
        c3.innerHTML = "<b>SIMILARITY: </b>" +similarity;

        firstRow.appendChild(c1);
        firstRow.appendChild(c2);
        firstRow.appendChild(c3);

       // txtContent = txtContent + "SCORE: "+socre + "\t" + "E-VALUE: "+ evalue + "\t" +"SIMILARITY: "+ similarity + "\v";

        divResults.appendChild(firstRow);
        var array = alignment.alignment.split('>');
        var sequence1 =array[1];
        var sequence2 =array[2];
        var sequence1Name = sequence1.split('\n')[0];
        sequence1Name = sequence1Name.split(' ')[0];
        var sequence2Name = sequence2.split('\n')[0];
        sequence2Name = sequence2Name.split(' ')[0];
        console.log(sequence1.split('\n',2));
        var sequence1Content = getContent(sequence1);
        var sequence2Content = getContent(sequence2);

        var seq1start = alignment.queryStart;
        var seq2start = alignment.hitStart;
        var length= 50;
        var iteration = 0;

        var middleSeq ="";

        for (var j =0; j < max(sequence1Content.length, sequence2Content.length); j++) {
            if (sequence1Content[j] && sequence2Content[j]){
                if (sequence1Content[j] == sequence2Content[j]){
                    middleSeq = middleSeq + "|";
                }else{
                    middleSeq = middleSeq + ".";
                }
            }else{
                middleSeq = middleSeq + ".";

            }
        }
        var chunkedSeq1 = sequence1Content.match(/.{1,50}/g);
        var chunkedSeq2 = sequence2Content.match(/.{1,50}/g);
        var chunkedMiddle = middleSeq.match(/.{1,50}/g);

        for (var i =0; i < chunkedMiddle.length; i++) {
            var s1name = document.createElement("div");
            s1name.setAttribute("class", "col-md-3");
            var s1content = document.createElement("div");
            s1content.setAttribute("class", "col-md-7");
            var s1end = document.createElement("div");
            s1end.setAttribute("class", "col-md-2");
            var seq1StartValue="";
            if (chunkedSeq1[i]){
                s1content.innerHTML = chunkedSeq1[i];
                seq1StartValue = seq1start + chunkedSeq1[i].length *i+1;
                s1end.innerHTML = seq1StartValue-1 + chunkedSeq1[i].length;
            }else{
                s1content.innerHTML = " ";
                seq1StartValue =" "
                s1end.innerHTML = " ";
            }

            s1name.innerHTML = sequence1Name +"   "+ seq1StartValue;

            var row1 = document.createElement("div");
            row1.setAttribute("class","flex-row");
            row1.appendChild(s1name);
            row1.appendChild(s1content);
            row1.appendChild(s1end);

           // txtContent = txtContent + s1name + "\t"
            var middle1 = document.createElement("div");
            middle1.setAttribute("class", "col-md-3");
            var middle2 = document.createElement("div");
            middle2.setAttribute("class", "col-md-7");
            middle2.innerHTML = chunkedMiddle[i];
            var middle3 = document.createElement("div");
            middle3.setAttribute("class", "col-md-2");


            var row2 = document.createElement("div");
            row2.setAttribute("class","flex-row");
            row2.appendChild(middle1);
            row2.appendChild(middle2);
            row2.appendChild(middle3);

            var s2name = document.createElement("div");
            s2name.setAttribute("class", "col-md-3");
            var s2content = document.createElement("div");
            s2content.setAttribute("class", "col-md-7");
            var s2end = document.createElement("div");
            s2end.setAttribute("class", "col-md-2");
            var seq2StartValue="";
            if (chunkedSeq2[i]){
                s2content.innerHTML = chunkedSeq2[i];
                seq2StartValue = seq2start + chunkedSeq2[i].length *i+1;
                s2end.innerHTML = seq2StartValue-1 + chunkedSeq2[i].length;
            }else{
                s2content.innerHTML = " ";
                seq2StartValue =" "
                s2end.innerHTML = " ";
            }
            s2name.innerHTML = sequence2Name +"   "+ seq2StartValue;

            var row3 = document.createElement("div");
            row3.setAttribute("class","flex-row");
            row3.appendChild(s2name);
            row3.appendChild(s2content);
            row3.appendChild(s2end);

            divResults.appendChild(row1);
            divResults.appendChild(row2);
            divResults.appendChild(row3);
        }
        divResults.removeAttribute("hidden");
        var divDownload = document.getElementById("downloadResults");
        divDownload.removeAttribute("hidden");

    }
}

function showResults__(){
   var results=document.getElementById("results-input").value;
   var divResults = document.getElementById("table-results");
    if (results.length>0){
        results = JSON.parse(results);
        console.log(results)
        var alignment = results[results.length-1]

        var score =  alignment.score;
        var evalue = alignment.evalue;
        var similarity = alignment.similarity;

        var firstRow = document.createElement("div");
        firstRow.setAttribute("class","flex-row separated");
        var c1 = document.createElement("div");
        c1.setAttribute("class","col-md-4");
        c1.innerHTML = "<b>SCORE: </b>"+score;
        var c2 = document.createElement("div");
        c2.setAttribute("class","col-md-4");
        c2.innerHTML = "<b>E-VALUE: </b>"+ evalue;
        var c3 = document.createElement("div");
        c3.setAttribute("class","col-md-4");
        c3.innerHTML = "<b>SIMILARITY: </b>" +similarity;

        firstRow.appendChild(c1);
        firstRow.appendChild(c2);
        firstRow.appendChild(c3);

        divResults.appendChild(firstRow);
        var array = alignment.alignment.split('>');
        var sequence1 =array[1];
        var sequence2 =array[2];
        var sequence1Name = sequence1.split('\n')[0];
        sequence1Name = sequence1Name.split(' ')[0];
        var sequence2Name = sequence2.split('\n')[0];
        sequence2Name = sequence2Name.split(' ')[0];
        console.log(sequence1.split('\n',2));
        var sequence1Content = getContent(sequence1);
        var sequence2Content = getContent(sequence2);

        var seq1start = alignment.queryStart;
        var seq2start = alignment.hitStart;
        var length= 50;
        var iteration = 0;

        var middleSeq ="";

        for (var j =0; j < max(sequence1Content.length, sequence2Content.length); j++) {
            if (sequence1Content[j] && sequence2Content[j]){
                if (sequence1Content[j] == sequence2Content[j]){
                    middleSeq = middleSeq + "|";
                }else{
                    middleSeq = middleSeq + ".";
                }
            }else{
                middleSeq = middleSeq + ".";

            }
        }
        var chunkedSeq1 = sequence1Content.match(/.{1,50}/g);
        var chunkedSeq2 = sequence2Content.match(/.{1,50}/g);
        var chunkedMiddle = middleSeq.match(/.{1,50}/g);

        var table = document.createElement("table");
        table.setAttribute("id", "table_results");
        table.setAttribute("class", "table table-striped");
        var thead = document.createElement("thead");
        var th = thead.insertRow(-1);
        var th1 = document.createElement("th");
        th1.innerHTML = "Name";
        th.appendChild(th1);
        var th2= document.createElement("th");
        th2.innerHTML = "Start";
        th.appendChild(th2);
        var th3 = document.createElement("th");
        th3.innerHTML = "Alignment";
        th.appendChild(th3);
        var th4 = document.createElement("th");
        th4.innerHTML = "End";
        th.appendChild(th4);
        table.appendChild(thead);

        var tbody = document.createElement("tbody");
        table.appendChild(tbody);

        for (var i =0; i < chunkedMiddle.length; i++) {
           /* var s1name = document.createElement("div");
            s1name.setAttribute("class", "col-md-3");
            var s1content = document.createElement("div");
            s1content.setAttribute("class", "col-md-7");
            var s1end = document.createElement("div");
            s1end.setAttribute("class", "col-md-2");
            var seq1StartValue="";
            if (chunkedSeq1[i]){
                s1content.innerHTML = chunkedSeq1[i];
                seq1StartValue = seq1start + chunkedSeq1[i].length *i+1;
                s1end.innerHTML = seq1StartValue-1 + chunkedSeq1[i].length;
            }else{
                s1content.innerHTML = " ";
                seq1StartValue =" "
                s1end.innerHTML = " ";
            }
            s1name.innerHTML = sequence1Name +"   "+ seq1StartValue;
*/
            var tr1 = tbody.insertRow(-1);

            var s1name = tr1.insertCell(-1);
            var s1start = tr1.insertCell(-1);
            var s1content = tr1.insertCell(-1);
            var s1end = tr1.insertCell(-1);

            if (chunkedSeq1[i]){
                s1content.innerHTML = chunkedSeq1[i];
                seq1StartValue = seq1start + chunkedSeq1[i].length *i+1;
                s1end.innerHTML = seq1StartValue-1 + chunkedSeq1[i].length;
            }else{
                s1content.innerHTML = " ";
                seq1StartValue =" "
                s1end.innerHTML = " ";
            }
            s1name.innerHTML = sequence1Name;
            s1start.innerHTML = seq1StartValue;

/*            var row1 = document.createElement("div");
            row1.setAttribute("class","flex-row");
            row1.appendChild(s1name);
            row1.appendChild(s1content);
            row1.appendChild(s1end);*/

           // txtContent = txtContent + s1name + "\t"
            /*var middle1 = document.createElement("div");
            middle1.setAttribute("class", "col-md-3");
            var middle2 = document.createElement("div");
            middle2.setAttribute("class", "col-md-7");
            middle2.innerHTML = chunkedMiddle[i];
            var middle3 = document.createElement("div");
            middle3.setAttribute("class", "col-md-2");


            var row2 = document.createElement("div");
            row2.setAttribute("class","flex-row");
            row2.appendChild(middle1);
            row2.appendChild(middle2);
            row2.appendChild(middle3);*/


            var tr2 = tbody.insertRow(-1);
            var middleName = tr2.insertCell(-1);
            var middleStart = tr2.insertCell(-1);
            var middleContent = tr2.insertCell(-1);
            var middleEnd = tr2.insertCell(-1);

            middleName.innerHTML="";
            middleStart.innerHTML="";
            middleContent.innerHTML=chunkedMiddle[i];
            middleEnd.innerHTML="";

          /*  var s2name = document.createElement("div");
            s2name.setAttribute("class", "col-md-3");
            var s2content = document.createElement("div");
            s2content.setAttribute("class", "col-md-7");
            var s2end = document.createElement("div");
            s2end.setAttribute("class", "col-md-2");
            var seq2StartValue="";
            if (chunkedSeq2[i]){
                s2content.innerHTML = chunkedSeq2[i];
                seq2StartValue = seq2start + chunkedSeq2[i].length *i+1;
                s2end.innerHTML = seq2StartValue-1 + chunkedSeq2[i].length;
            }else{
                s2content.innerHTML = " ";
                seq2StartValue =" "
                s2end.innerHTML = " ";
            }
            s2name.innerHTML = sequence2Name +"   "+ seq2StartValue;

            var row3 = document.createElement("div");
            row3.setAttribute("class","flex-row");
            row3.appendChild(s2name);
            row3.appendChild(s2content);
            row3.appendChild(s2end);

            divResults.appendChild(row1);
            divResults.appendChild(row2);
            divResults.appendChild(row3);*/

            var tr3 = tbody.insertRow(-1);

            var s2name = tr3.insertCell(-1);
            var s2start = tr3.insertCell(-1);
            var s2content = tr3.insertCell(-1);
            var s2end = tr3.insertCell(-1);
            if (chunkedSeq2[i]){
                s2content.innerHTML = chunkedSeq2[i];
                seq2StartValue = seq2start + chunkedSeq2[i].length *i+1;
                s2end.innerHTML = seq2StartValue-1 + chunkedSeq2[i].length;
            }else{
                s2content.innerHTML = " ";
                seq2StartValue =" "
                s2end.innerHTML = " ";
            }
            s2name.innerHTML = sequence2Name;
            s2start.innerHTML = seq2StartValue;
        }
        table.setAttribute("style",'font-family: "Courier New", Courier, monospace; font-size: 14px;');
        divResults.appendChild(table);
        divResults.removeAttribute("hidden");
        var divDownload = document.getElementById("downloadResults");
        divDownload.removeAttribute("hidden");

    }
}

function showResults(){
   var results=document.getElementById("results-input").value;
   var divResults = document.getElementById("table-results");
    if (results.length>0){
        results = JSON.parse(results);
        console.log(results)
        var alignment = results[results.length-1]

        var score =  alignment.score;
        var evalue = alignment.evalue;
        var similarity = alignment.similarity;

        //var txtContent = "";
        var firstRow = document.createElement("div");
        firstRow.setAttribute("class","flex-row separated");
        var c1 = document.createElement("div");
        c1.setAttribute("class","col-md-4");
        c1.innerHTML = "<b>SCORE: </b>"+score;
        var c2 = document.createElement("div");
        c2.setAttribute("class","col-md-4");
        c2.innerHTML = "<b>E-VALUE: </b>"+ evalue;
        var c3 = document.createElement("div");
        c3.setAttribute("class","col-md-4");
        c3.innerHTML = "<b>SIMILARITY: </b>" +similarity;

        firstRow.appendChild(c1);
        firstRow.appendChild(c2);
        firstRow.appendChild(c3);
        var r = {"SCORE": score, "EVALUE":evalue, "SIMILARITY": similarity};
        console.log(r);
        rows1.push(r);

        divResults.appendChild(firstRow);
        var array = alignment.alignment.split('>');
        var sequence1 =array[1];
        var sequence2 =array[2];
        var sequence1Name = sequence1.split('\n')[0];
        sequence1Name = sequence1Name.split(' ')[0];
        var sequence2Name = sequence2.split('\n')[0];
        sequence2Name = sequence2Name.split(' ')[0];
        console.log(sequence1.split('\n',2));
        var sequence1Content = getContent(sequence1);
        var sequence2Content = getContent(sequence2);

        var seq1start = alignment.queryStart;
        var seq2start = alignment.hitStart;
        var length= 50;
        var iteration = 0;

        var middleSeq ="";

        for (var j =0; j < max(sequence1Content.length, sequence2Content.length); j++) {
            if (sequence1Content[j] && sequence2Content[j]){
                if (sequence1Content[j] == sequence2Content[j]){
                    middleSeq = middleSeq + "|";
                }else{
                    middleSeq = middleSeq + ".";
                }
            }else{
                middleSeq = middleSeq + ".";

            }
        }
        var chunkedSeq1 = sequence1Content.match(/.{1,50}/g);
        var chunkedSeq2 = sequence2Content.match(/.{1,50}/g);
        var chunkedMiddle = middleSeq.match(/.{1,50}/g);

        for (var i =0; i < chunkedMiddle.length; i++) {
            var s1name = document.createElement("div");
            s1name.setAttribute("class", "col-md-3");
            var s1content = document.createElement("div");
            s1content.setAttribute("class", "col-md-7");
            var s1end = document.createElement("div");
            s1end.setAttribute("class", "col-md-2");
            var seq1StartValue="";
            var s1contentValue="";
            var s1endValue ="";
            if (chunkedSeq1[i]){
                s1contentValue= chunkedSeq1[i];
                seq1StartValue = seq1start + chunkedSeq1[i].length *i+1;
                s1endValue = seq1StartValue-1 + chunkedSeq1[i].length;
            }else{
                s1contentValue = " ";
                seq1StartValue =" "
                s1endValue = " ";
            }

            s1name.innerHTML = sequence1Name +"   "+ seq1StartValue;
            s1content.innerHTML = s1contentValue;
            s1end.innerHTML = s1endValue;

            var row1 = document.createElement("div");
            row1.setAttribute("class","flex-row");
            row1.appendChild(s1name);
            row1.appendChild(s1content);
            row1.appendChild(s1end);

            var middle1 = document.createElement("div");
            middle1.setAttribute("class", "col-md-3");
            var middle2 = document.createElement("div");
            middle2.setAttribute("class", "col-md-7");
            middle2.innerHTML = chunkedMiddle[i];
            var middle3 = document.createElement("div");
            middle3.setAttribute("class", "col-md-2");


            var row2 = document.createElement("div");
            row2.setAttribute("class","flex-row");
            row2.appendChild(middle1);
            row2.appendChild(middle2);
            row2.appendChild(middle3);

            var s2name = document.createElement("div");
            s2name.setAttribute("class", "col-md-3");
            var s2content = document.createElement("div");
            s2content.setAttribute("class", "col-md-7");
            var s2end = document.createElement("div");
            s2end.setAttribute("class", "col-md-2");
            var s2contentValue="";
            var seq2StartValue="";
            var s2endValue = "";
            if (chunkedSeq2[i]){
                s2contentValue = chunkedSeq2[i];
                seq2StartValue = seq2start + chunkedSeq2[i].length *i+1;
                s2endValue = seq2StartValue-1 + chunkedSeq2[i].length;
            }else{
                s2contentValue = " ";
                seq2StartValue =" "
                s2endValue = " ";
            }
            s2name.innerHTML = sequence2Name +"   "+ seq2StartValue;
            s2content.innerHTML = s2contentValue;
            s2end.innerHTML = s2endValue;
            var row3 = document.createElement("div");
            row3.setAttribute("class","flex-row");
            row3.appendChild(s2name);
            row3.appendChild(s2content);
            row3.appendChild(s2end);

            divResults.appendChild(row1);
            divResults.appendChild(row2);
            divResults.appendChild(row3);
            var r1 = {"Name": sequence1Name, "Start": seq1StartValue, "Alignment": s1contentValue, "End":s1endValue };
            var r2 = {"Name": " ", "Start": " ", "Alignment": chunkedMiddle[i], "End": " "};
            var r3 = {"Name": sequence2Name, "Start": seq2StartValue, "Alignment": s2contentValue, "End":s2endValue};
            rows2.push(r1);
            rows2.push(r2);
            rows2.push(r3);
        }
        divResults.removeAttribute("hidden");
        var divDownload = document.getElementById("downloadResults");
        divDownload.removeAttribute("hidden");

    }
}

function showUserMenu(){
    var menu = document.getElementById("user-menu");
    if (menu.getAttribute('hidden') == null) {
        menu.setAttribute('hidden', "true");

    }
    else{
       menu.removeAttribute("hidden");
    }
}

function toLogin(){
window.location.replace('/');
}

function downloadInnerHtml2() {
    var data = [],fontSize = 11,height = 0,doc;

    doc = new jsPDF('p', 'pt', 'a4', true);
    doc.setFont("courier", "normal");
    doc.setFontSize(fontSize);
    doc.text(50,100,"hi table");
    for (var insert = 0; insert <= 20; insert++) {
		data.push({
			"name" : "jspdf plugin",
			"version" : insert,
			"author" : "Prashanth Nelli",
			"Designation" : "AngularJs Developer"
		});
	}
	height = doc.drawTable(data, {xstart:10,ystart:10,tablestart:70,marginleft:50});
	doc.text(50, height + 20, 'hi world');
	doc.save("some-file.pdf");
}

function downloadInnerHtml_() {

        var pdf = new jsPDF('p', 'pt', 'letter');

        source = $('#table-results')[0];
        pdf.setFont("courier new monospace");
        pdf.setFontSize(11);

        specialElementHandlers = {
            // element with id of "bypass" - jQuery style selector
            '#bypassme': function (element, renderer) {
                // true = "handled elsewhere, bypass text extraction"
                return true
            }
        };
        margins = {
            top: 80,
            bottom: 60,
            left: 30,
            width: 800
        };
        // all coords and widths are in jsPDF instance's declared units
        // 'inches' in this case
        pdf.fromHTML(
            source, // HTML string or DOM elem ref.
            margins.left, // x coord
            margins.top, { // y coord
                'width': margins.width, // max width of content on PDF
                'elementHandlers': specialElementHandlers
            },

            function (dispose) {
                // dispose: object with X, Y of the last line add to the PDF
                //          this allow the insertion of new lines after html
                pdf.save('Test.pdf');
            }, margins
        );
    }


function downloadInnerHtml(){
const doc = new jsPDF('p', 'pt');
// according to jspdf, PTSans must be base64 font, full string is on jsPDF/examples/js/basic.js

doc.setFont('Courier', '');
doc.setFontSize(11);

doc.autoTable(columns1, rows1, {
    theme: 'grid',
    styles: {
        fontSize: 10,
        font: 'Courier'
    },
    headStyles:{
        valign: 'middle',
        halign : 'center'
    },
    columnStyles: {
        SCORE: {
            halign: "center",
            font: 'Courier',
        },
        EVALUE: {
            halign: "center",
            font: 'Courier'
        },
        SIMILARITY: {
            halign: "center",
            font: 'Courier'
        }
    },
    cellWidth: 'auto'
});

doc.autoTable(columns2, rows2, {
    theme: 'plain',
    styles: {
        fontSize: 10,
        font: 'Courier'
    },
    columnStyles: {
        font: 'Courier',
        Name: {
            halign: "center",
            font: 'Courier'
        },
        Start: {
            halign: "center",
            font: 'Courier'
        },
        Alignment: {
            halign: "left",
            font: 'Courier'
        },
         End: {
            halign: "center",
            font: 'Courier'
        }
    },
    tableWidth: 'wrap',
    showHeader: 'always',
});

console.log(doc.getFontList());
doc.save('alignment-result.pdf');
}


function controlUploadButton(){
    var dbname = document.getElementById('dbname');
    var files = document.getElementById('dbfiles');

    dbname.addEventListener('change', validateForm);
    files.addEventListener('change', validateForm);
    validateForm();
}

function validateForm(){
  var submit = document.getElementById('submit');
  var dbname = document.getElementById('dbname').value;
  var files = document.getElementById('dbfiles').value;

  if(dbname==="" || files.length==0)
    submit.setAttribute("disabled",true);
  else
    submit.removeAttribute("disabled");
}
