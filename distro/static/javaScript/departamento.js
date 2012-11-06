//Variavel que guarda o docente selecionado
var selectedTeacher = null;

//Variavel que guarda o modulo selecionado
var modulTable = null;

//Array que guarda os modulos que tem docente adicionado
var added = new Array();
//Array que gaurda os modulos cujo o departamento foi delegado
var addedDep = new Array();


/**
 * Resposnavel por marcar um docente como selecionado
 * quando clicamos nele na lista de docentes
 * presente na area de atribuição de
 * modulos
 * 
 * @param {Object} obj - Docente
 */
function highlight(obj) {
	if (selectedTeacher != null) {

		selectedTeacher.className = "docenteRow";
	}

	obj.className += " select";

	selectedTeacher = obj;

}
/**
 * Resposavel por marcar como selecionado
 * o modulo quando clicado nele
 * 
 * @param {Object} obj - Modulo
 */
function highlightModul(obj) {

	if (modulTable != null) {

		modulTable.className = "tabela_sumario modulsTable";

		var count = 0;

		for (var i = 0; i < addedDep.length; i++) {
			//alert(addedDep[i]);

			if (addedDep[i] == modulTable) {

				count += 1;

			}
		}

		//alert(count + " - Cima");

		if (count == 0) {
			
			if(modulTable.rows[3].className != "showDelegate blockDelegate")
		{
			modulTable.rows[3].className = "hideDelegate";
		}else
		{
			
		}

		}

	}
	//Verificação se o modulos tem escolha de departamento
	modulTable = obj;
	count = 0;
	for (var j = 0; j < addedDep.length; j++) {
			if (addedDep[j] == modulTable) {
				count += 1;
			}
		}
	

	
	if (count == 0)
	 {
	 	//obj.className != "tabela_sumario modulsTable haveDelegate" && obj.rows[3].cells[0].childNodes[0].value == null
		//alert("aqui");
		modulTable.className = "tabela_sumario selectModulo";
		
		if(modulTable.rows[3].className != "showDelegate blockDelegate")
		{
		
		

		

		/*var nRows = modulTable.rows.length;

		 var newRow = modulTable.insertRow(3);
		 newCell1 = newRow.insertCell(0);
		 newCell1.colSpan = "2";
		 newCell1.innerHTML = '<a href="#" >Delgar a outro departamento</a>';
		 newCell2 = newRow.insertCell(1);
		 newCell2.innerHTML = '<a href="#" ><img src="/static/images/icons/changeDep.png" /></a>';*/

		

		

		//alert(count + " - baixo");
		

			var nRows = modulTable.rows[3];

			nRows.className = "showDelegate";

			newCell1 = nRows.cells[1];
			newCell1.colSpan = "2";
			newCell1.innerHTML = '<a onclick="addComboToDelegate(this.parentNode.parentNode);" href="#" >Delgar a outro departamento</a>';

			newCell2 = nRows.cells[2];
			newCell2.innerHTML = '<a onclick="addComboToDelegate(this.parentNode.parentNode);" href="#" ><img src="/static/images/icons/changeDep.png" /></a>';
	
		}else
		{
			
			
		}
		
	}else
	{
		modulTable = null;
	}
	//alert(addedDep);

}

/**
 * Quando se verifica que existe um modulo selecionado
 * e um docente selecionado
 * é permitido a adição de um docente ao modulo
 */
function addDocente_to_modul() {
	//Detecta modificação na pagina de confirmação e volta a colcoar o botão de adicionar
	testeSearch();
	
	if (modulTable != null) {
		modulTable.className = "tabela_sumario modulsTable";
	}

	if (selectedTeacher != null) {
		selectedTeacher.className = "docenteRow";

	}

	var nRows = modulTable.rows.length;

	if (modulTable != null && selectedTeacher != null && modulTable.rows[2].cells[1].innerHTML == "") {

		var numOfCols = modulTable.rows[nRows - 1].cells.length;

		var newRow = modulTable.rows[2];

		newCell1 = newRow.cells[0];
		newCell1.innerHTML = "<input type='text' name='docenteID[]' value=" + selectedTeacher.cells[0].innerHTML + " />";
		newCell2 = newRow.cells[1];
		newCell2.innerHTML = selectedTeacher.cells[1].innerHTML;
		newCell3 = newRow.cells[2];
		newCell3.innerHTML = selectedTeacher.cells[2].innerHTML;
		newCell4 = newRow.cells[3];
		newCell4.innerHTML = "<a href='#' onclick='deleteRowTable(this.parentNode.parentNode.parentNode);'><span class='delButton'></span></a>";

		var nPos = added.length;

		added[nPos] = selectedTeacher;

		selectedTeacher.className += " added"
		selectedTeacher = null;

		modulTable = null;
		
		
		
		
	}
}

/*function contains(arr, findValue) {
 var i = arr.length;

 while (i--) {
 if (arr[i] === findValue) return true;
 }
 return false;
 }*/

/**
 * Elimina o docente introduzido num
 * modulo quando clicado no botão eliminar
 * 
 * @param {Object} obj - Modulo do botão
 */
function deleteRowTable(obj) {
	
	
	if(obj.parentNode.className != "tabela_sumario modulsTable haveDelegate")
	{
	//Detecta modificação na pagina de confirmação e volta a colcoar o botão de adicionar
	testeSearch();
	
	var row = obj.rows[2];

	if (row.cells[0].childNodes[1] != null) {
		//alert("true");
		var idValue_main = row.cells[0].childNodes[1].value;

	} else if (row.cells[0].childNodes[0] != null) {
		//alert("false");
		var idValue_main = row.cells[0].childNodes[0].value;

	}

	//alert(idValue_main);

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

	obj.row[3].className = "hideDelegate";
	}
	
	
	
	
	
	
}

/**
 * Função carregada inicialmente 
 * que verifica o HTML e verifica 
 * quais os docentes ja com modulos
 * os modulos
 * delegados
 * Inicializando assim as variaveis
 */
function initial() {

	var teachersId = new Array();

	var table = document.getElementsByClassName("modulsTable");

	for (var i = 0; i < table.length; i++) {

		if (table[i].rows[2].cells[0].childNodes[0].value != null && table[i].rows[2].cells[0].childNodes[0].value != "") {
			teachersId[i] = table[i].rows[2].cells[0].childNodes[0].value;

		} else if (table[i].rows[2].cells[0].childNodes[1].value != null && table[i].rows[2].cells[0].childNodes[1].value != "") {

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

	for (var l = 0; l < table.length; l++) {
		
		
		
		
		if (table[l].className == "tabela_sumario modulsTable haveDelegate" || table[l].rows[3].cells[0].childNodes[0].value != null) {

	
			addedDep[l] = table[l];

		} else {
			addedDep[l] = 0;
		}
		

	}
	
	//alert(addedDep);

}

/**
 * Quando selecionado um modulo
 * e clicamos no botão de delegação de
 * departamento
 * é feita uma chamada de AJAX
 * que nos permite obter a lista de departamentos
 * os quais sao permitidos delegar
 */
function addComboToDelegate(obj) {

	require(["dojo/request", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, on, dom) {

		request.get("combotodelegate").then(function(response) {
			modulTable.className = "tabela_sumario modulsTable";
			modulTable = null;
			
			obj.innerHTML = response;
			addedDep[addedDep.length] = obj.parentNode.parentNode;
			
			deleteRowTable(obj.parentNode.parentNode);
			
			
			//alert(addedDep);

		}, function(error) {
			// Display the error returned
			alert(response);
		});

	});
}
/**
 * Quando eliminamos a delegação 
 * voltamos a ter novamente o botao de
 * delegação
 * @param {Object} obj - Linha do botão na tabela do modulo
 */
function rolebackDelegate(obj) {

	//Detecta modificação na pagina de confirmação e volta a colcoar o botão de adicionar
	testeSearch();
	
	for (var i = 0; i < addedDep.length; i++) 
	{
		if (obj.parentNode.parentNode == addedDep[i]) {
			addedDep.splice(i, 1);
		}
	}

	obj.innerHTML = '<td class="idHide" ><input type="hidden" name="delegateDep[]" value="0" /></td><td colspan="2"></td><td></td>';
	
	
	
		
}
