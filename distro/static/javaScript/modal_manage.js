$list_modal = [];
$n_elements = -1;

function addToModalList($modal)
{

	//oculta todos
	
	if($n_elements >= 0)
	{
		for($modal in $list_modal)
		{
			
			
			$($modal).modal("hide");
		}
	}
	/***************************/
	//adiciona ao body o modal
	$("body").append($modal);
	
	//vai buscalo para o colocar na lista
	$n = $(".modal").length;
	
	$list_modal.push($(".modal").eq($n - 1));
	
	//acrescenta o contador da lista
	$n_elements += 1;
	
	
	//mostra o com o metodo
	showModal($list_modal[$n_elements]);
	
}

function showModal($modal)
{
	
	

	$($modal).modal({
					
					backdrop: "static",
					show: true
					});
					
	load_cancel_event();
}

function re_showModal($modal)
{
	
	

	$($modal).modal("show");
}

function cancelModal()
{
	
	//console.log("Cancel Inicio "+$n_elements); 
	
$modal = $list_modal[$n_elements];




$($modal).on('hidden.bs.modal', function (e) {
	
						$list_modal.pop();
	 					$($modal).remove();
	 					$n_elements -= 1;
	 					//console.log("Pre ELiminar "+$n_elements); 
	 					if($n_elements >= 0)
	 					{
	 						re_showModal($list_modal[$n_elements]);
	 						
	 					}
	 					
	 					//console.log("ELiminar "+$n_elements);
					});


$($modal).modal("hide");

//console.log("Cancel Fim "+$n_elements); 
//console.log("Cancel Fim "+$list_modal.length); 
	
}


function addToModalList_after_cancel($arg)
{
	

	
$modal = $list_modal[$n_elements];




$($modal).on('hidden.bs.modal', function (e) {
	
						$list_modal.pop();
	 					$($modal).remove();
	 					$n_elements -= 1;
	 	
	 					addToModalList($arg);
	 		
					});


$($modal).modal("hide");


	
}


function load_cancel_event()
{
	$( ".modal_cancel" ).click(function() {
	

	cancelModal();
	
	
	});
	
}



