var selectedTeacher = null;

var modulTable = null;

var added = new Array();

function highlight(obj) {
	if (selectedTeacher != null) {
		selectedTeacher.className = "docenteRow";
	}

	obj.className += " select";

	selectedTeacher = obj;

}

function highlightModul(obj) {
	if (modulTable != null) {
		modulTable.className = "tabela_sumario modulsTable";
	}

	obj.className = "tabela_sumario selectModulo";

	modulTable = obj;
}

function addDocente_to_modul() {
	if (modulTable != null) {
		modulTable.className = "tabela_sumario modulsTable";
	}

	if (selectedTeacher != null) {
		selectedTeacher.className = "docenteRow";

	}

	var nRows = modulTable.rows.length;

	if (modulTable != null && selectedTeacher != null) {

		var numOfCols = modulTable.rows[nRows - 1].cells.length;

		var newRow = modulTable.rows[2];

		newCell1 = newRow.cells[0]
		newCell1.innerHTML = "<input type='text' name='docenteID[]' value=" + selectedTeacher.cells[0].innerHTML + " />";
		newCell2 = newRow.cells[1]
		newCell2.innerHTML = selectedTeacher.cells[1].innerHTML;
		newCell3 = newRow.cells[2]
		newCell3.innerHTML = selectedTeacher.cells[2].innerHTML;
		newCell4 = newRow.cells[3]
		newCell4.innerHTML = "<a href='#' onclick='deleteRowTable(this.parentNode.parentNode.parentNode);'><span class='delButton'></span></a>";

		var nPos = added.length;

		added[nPos] = selectedTeacher;

		selectedTeacher.className += " added"
		selectedTeacher = null;

		modulTable = null;
	}
}

function deleteRowTable(obj) {

	var row = obj.rows[2];

	var idValue_main = row.cells[0].childNodes[0].value;

	for (var i = 0; i < added.length; i++) {
		var idValeu = added[i].cells[0].innerHTML;

		if (idValue_main == idValeu) {

			added[i].className = "";
			added.splice(i, 1);
		}
	}

	row.cells[0].innerHTML = "<input type='text' name='docenteID[]' value='' />";
	row.cells[1].innerHTML = "";
	row.cells[2].innerHTML = "";
	row.cells[3].innerHTML = "";

}

function initial() {

	var teachersId = new Array();

	var table = document.getElementsByClassName("modulsTable");

	for (var i = 0; i < table.length; i++) {

		if (table[i].rows[2].cells[0].childNodes[0].value != null && table[i].rows[2].cells[0].childNodes[0].value != "") 
		{
			teachersId[i] = table[i].rows[2].cells[0].childNodes[0].value;
			
		} else if (table[i].rows[2].cells[0].childNodes[1].value != null && table[i].rows[2].cells[0].childNodes[1].value != "") 
		{
			

			teachersId[i] = table[i].rows[2].cells[0].childNodes[1].value;
			

		}
	}

	//alert(teachersId);
	
	var tableTeachers = document.getElementsByClassName("teachersTable")[0];

	for (var j = 0; j < tableTeachers.rows.length; j++) {
		var row = tableTeachers.rows[j];

		for (var k = 0; k < teachersId.length; k++) {
			if (row.cells[0].innerHTML == teachersId[k]) {
				added[added.length] = row;
				row.className += " added";
			}
		}
	}

}
