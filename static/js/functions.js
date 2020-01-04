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
