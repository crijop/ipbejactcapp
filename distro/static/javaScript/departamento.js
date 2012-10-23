var td1 = null;
var td2 = null;

var modulTable = null;

function highlight(obj) {
	if (td1 != null || td2 != null) {
		td1.className = null;
		td2.className = null;
	}

	obj.cells[1].className += "select";
	obj.cells[2].className += "select";
	
	td1 = obj.cells[1];
	td2 = obj.cells[2];
	
	
}


function highlightModul(obj) {
	if (modulTable != null) {
		modulTable.className = "tabela_sumario modulsTable";
	}

	obj.className += " selectModulo";

	modulTable = obj;
}


function addDocente_to_modul() {
	if (modulTable != null) {
		modulTable.className = "tabela_sumario modulsTable";
	}
	
	if (td1 != null || td2 != null) {
		td1.className = null;
		td2.className = null;
	}

	
	
	var nRows = modulTable.rows.length;

	var numOfCols = modulTable.rows[nRows - 1].cells.length;


	var newRow = modulTable.insertRow(nRows);

	newCell1 = newRow.insertCell(0);
	newCell1.innerHTML = td1.innerHTML;
	newCell2 = newRow.insertCell(1);
	newCell2.innerHTML = td2.innerHTML;
	
td1 = null;
td2 = null;

modulTable = null;
}