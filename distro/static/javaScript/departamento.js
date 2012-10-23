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

	obj.className += " selectModulo";

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

	if(nRows < 3)
	{

	var numOfCols = modulTable.rows[nRows - 1].cells.length;


	var newRow = modulTable.insertRow(nRows);

	
	newCell1 = newRow.insertCell(0);
	newCell1.innerHTML = "<input type='text' name='docenteID[]' value=" + selectedTeacher.cells[0].innerHTML + " />";
	newCell1.className += "idHide";
	newCell2 = newRow.insertCell(1);
	newCell2.innerHTML = selectedTeacher.cells[1].innerHTML;
	newCell3 = newRow.insertCell(2);
	newCell3.innerHTML = selectedTeacher.cells[2].innerHTML;
	newCell4 = newRow.insertCell(3);
	newCell4.innerHTML = "<a href='#' onclick='deleteRowTable(this.parentNode.parentNode.rowIndex, this.parentNode.parentNode.parentNode);'><span class='delButton'></span></a>";

		
	var nPos = added.length;
	
	added[nPos] = selectedTeacher;	
		
	selectedTeacher.className += " added"	
	selectedTeacher = null;

	modulTable = null;
	}
}

function deleteRowTable(index, obj) 
{
	var row = obj.rows[2];
	var idValue_main = row.cells[0].childNodes[0].value;
	
	for(var i = 0; i < added.length; i++)
	{
		var idValeu = added[i].cells[0].innerHTML;
		if(idValue_main == idValeu)
		{
			added[i].className = "";
		}
	}
	obj.deleteRow(index);
}