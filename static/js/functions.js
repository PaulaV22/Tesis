var dbs= []

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
    table.setAttribute("class", "table table-hover table-condensed");
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
$("#close-sidebar").click(function() {
  $(".page-wrapper").removeClass("toggled");
});
$("#show-sidebar").click(function() {
  $(".page-wrapper").addClass("toggled");
});

});

function configureSideBar(){
    var username = document.getElementById("username").value;
    console.log(username);
    var span = document.getElementById("usernameSpan");
    span.innerHTML = username;
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
            divHeaderSubRow.className="row";
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
            divHeaderSubRow4.className="col-md-3 text-left";
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
               divSubRow.className="row";
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
    var div = document.getElementById("#show-sidebar");
    div.setAttribute("id","#close-sidebar");
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

function showResults(){
   var results=document.getElementById("results-input").value;
    if (results.length>0){
        results = JSON.parse(results);
        console.log(results)
        var alignment = results[results.length-1]

        var score =  alignment.score;
        var evalue = alignment.evalue;
        var similarity = alignment.similarity;


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

        console.log(chunkedSeq1);
        console.log(chunkedSeq2);
        console.log(chunkedMiddle);
        var divResults = document.getElementById("table-results");

        for (var i =0; i < chunkedMiddle.length; i++) {
            var s1name = document.createElement("div");
            s1name.setAttribute("class", "col-md-3");
            var s1content = document.createElement("div");
            s1content.setAttribute("class", "col-md-8");
            var s1end = document.createElement("div");
            s1end.setAttribute("class", "col-md-1");
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
            row1.setAttribute("class","row");
            row1.appendChild(s1name);
            row1.appendChild(s1content);
            row1.appendChild(s1end);

            var middle1 = document.createElement("div");
            middle1.setAttribute("class", "col-md-3");
            var middle2 = document.createElement("div");
            middle2.setAttribute("class", "col-md-8");
            middle2.innerHTML = chunkedMiddle[i];
            var middle3 = document.createElement("div");
            middle3.setAttribute("class", "col-md-1");


            var row2 = document.createElement("div");
            row2.setAttribute("class","row");
            row2.appendChild(middle1);
            row2.appendChild(middle2);
            row2.appendChild(middle3);

            var s2name = document.createElement("div");
            s2name.setAttribute("class", "col-md-3");
            var s2content = document.createElement("div");
            s2content.setAttribute("class", "col-md-8");
            var s2end = document.createElement("div");
            s2end.setAttribute("class", "col-md-1");
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
            row3.setAttribute("class","row");
            row3.appendChild(s2name);
            row3.appendChild(s2content);
            row3.appendChild(s2end);

            divResults.appendChild(row1);
            divResults.appendChild(row2);
            divResults.appendChild(row3);

        }
        /*divSeq1Content = document.getElementById("content1");
        divSeq1Content.innerHTML = sequence1Content;
        divSeq2Content = document.getElementById("content2");
        divSeq2Content.innerHTML = sequence2Content;*/
        divResults.removeAttribute("hidden")
    }


}