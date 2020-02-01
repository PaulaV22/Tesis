var dbs= []

function showLoading(){
    var seq = document.getElementById("sequence").value;
    document.getElementById("loader").removeAttribute("hidden");
    createTable();
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
    console.log(results);
    if (results.length!=0){
        results = JSON.parse(results);
        dbs = results;
        var thead = document.createElement("thead");
        var cols = ["Name", "Files", "Expand"];
        var tr = thead.insertRow(-1);


            var th1 = document.createElement("th");
            th1.innerHTML = "<b>NAME</b>";
            tr.appendChild(th1);

             var th2 = document.createElement("th");
            th2.innerHTML = "<b>FILES</b>";
            tr.appendChild(th2);

             var th3 = document.createElement("th");
            th3.innerHTML = "<b>DELETE</b>";
            tr.appendChild(th3);

             var th4 = document.createElement("th");
            th4.innerHTML = "<b>EXPAND</b>";
            tr.appendChild(th4);



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
            buttonDelete.setAttribute("data-toggle","collapse");
            buttonDelete.setAttribute("data-target", "#"+accordionId);
            buttonDelete.innerHTML = '<i class = "fa fa-trash-o"></i>';

            var tabCell3 = tr.insertCell(-1);
            //tabCell.appendChild(link);
            tabCell3.appendChild(buttonDelete);


            var accordionId = "accordion"+i

            var button = document.createElement("button");
            button.setAttribute("type", "button");
            button.className="button-icon";
            button.setAttribute("data-toggle","collapse");
            button.setAttribute("data-target", "#"+accordionId);
            button.innerHTML = '<i class = "fa  fa-angle-down"></i>';

            var tabCell4 = tr.insertCell(-1);
            //tabCell.appendChild(link);
            tabCell4.appendChild(button);

            var hiddenTr = tbody.insertRow(-1);
            hiddenTr.className="table-padding";
            hiddenTr.setAttribute("id", accordionId);
            hiddenTr.setAttribute("class", "collapse");

            var tabCellName = hiddenTr.insertCell(-1);
            var fileList = item["FileList"];
            tabCellName.setAttribute("colspan", fileList.length)

            //hidden row header
            var divHeaderRow = document.createElement("div");
            var divHeaderSubRow = document.createElement("div");
            divHeaderSubRow.className="row";
            var divHeaderSubRow1 = document.createElement("div");
            divHeaderSubRow1.className="col-5 text-left";
            divHeaderSubRow1.innerHTML = "<b>SEQUENCE NAME</b>";
            var divHeaderSubRow2 = document.createElement("div");
            divHeaderSubRow2.className="col-2 text-left";
            divHeaderSubRow2.innerHTML= "<b>SIZE</b>"
            var divHeaderSubRow3 = document.createElement("div");
            divHeaderSubRow3.className="col-2";
            divHeaderSubRow3.innerHTML="<b>INSPECT</b>"
            var divHeaderSubRow4 = document.createElement("div");
            divHeaderSubRow4.className="col-3 text-left";
            divHeaderSubRow4.innerHTML= "<b>DELETE SEQUENCE</b>"

            divHeaderSubRow.appendChild(divHeaderSubRow1);
            divHeaderSubRow.appendChild(divHeaderSubRow2);
            divHeaderSubRow.appendChild(divHeaderSubRow3);
            divHeaderSubRow.appendChild(divHeaderSubRow4);

            divHeaderRow.appendChild(divHeaderSubRow);

            tabCellName.appendChild(divHeaderRow);

            for (var k= 0; k < fileList.length -1; k++) {
               var fileInfo = fileList[k]
               var divRow = document.createElement("div");
               var divSubRow = document.createElement("div");
               divSubRow.className="row";
               var divSubRow1 = document.createElement("div");
               divSubRow1.className="col-5 text-left";
               divSubRow1.innerHTML = fileInfo["name"];
               var divSubRow2 = document.createElement("div");
               divSubRow2.className="col-2 text-left";
               divSubRow2.innerHTML= fileInfo["size"];
                var divSubRow3 = document.createElement("div");
               divSubRow3.className="col-2";

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
                divSubRow4.className="col-3";

                var buttonDelete = document.createElement("button");
                buttonDelete.setAttribute("type", "button");
                buttonDelete.className="button-icon";
                buttonDelete.setAttribute("id", i+"_"+k+"_delete");
                buttonDelete.innerHTML = '<i class = "fa  fa-trash-o"></i>';
                buttonDelete.addEventListener('click', function(){
                    var db = this.id.split('_')[0];
                    var file = this.id.split('_')[1];
                    var content = dbs[db]["FileList"][file]["content"];
                    var name = dbs[db]["FileList"][file]["name"];
                    showModal(name, content);
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
    var title = document.getElementById("modal-title");
    var body = document.getElementById("modal-body");

    title.innerHTML = name;
    body.innerHTML = content;
    $('#modalSequences').modal('show');
         // initializes and invokes show immediately
}