$ano = null;

function abrir_departamentos()
{
	
$.ajax({
      		type: "GET",
          	url:"/distro/vicp/ajax_abrir_lista_departamentos/",
          	success: function(response) {
            	
          
            	$(".table").after(response.html);
            	 /*$( ".teste_dialogo" ).dialog({
      				resizable: true,
      				draggable: false,
      				width:800,
      				modal: true,
      				title: "Dialog Title",
      				close: function()
      				{
      					$( ".teste_dialogo" ).remove();
      				}
			     
			    });*/
					
				$( ".teste_dialogo" ).modal({
					
					backdrop: "static",
					show: true
				});
				$('.teste_dialogo').on('hidden.bs.modal', function (e) {
 					$('.teste_dialogo').remove();
				});
	
					            	
            	/*$("#id_code").val(data.code);
            	$("#id_ip").val(data.ip);
            	$("#id_portatil").val(data.portatil);
            	var valorBool = data.portatil;
            	if (valorBool){
            		$(".imagemTF").attr("src", "/static/img/check_true.gif");
            	}
            	else{
            		$(".imagemTF").attr("src", "/static/img/check_false.png");
            	}*/
            	
            },
            error: function(rs, e) {
            	 
            	 
            	 
            }
     	});
	
}


function form_escolha_departamentos($ano)
{


                        var ids_Departamentos = [];
                        $('input:checked.checkable').each(function(){
                                var valor = $(this).val();
                                if(valor != undefined){
                                        ids_Departamentos.push(valor);
                                }
                        });
                       
                        //var ano = $("#inputAno").val();
                        var ano = $ano;
                        if (ids_Departamentos.length != 0){
                               
                                var target = "{%url ajax_save_lista_departamentos%}";
                                var csrftoken = getCookie('csrftoken');
                        $.ajax({
                                type: "POST",
                                url:target,
                                data: {"listaIdsDepartamento":ids_Departamentos, "ano":ano},
                                beforeSend: function( xhr ) {xhr.setRequestHeader("X-CSRFToken", csrftoken);},
                                success: function(data) {
                                        $( ".teste_dialogo" ).modal("toggle");
                                       
                                       
                                       
                                },
                            error: function(rs, e) {
                                 
                            }
                        });
                        }
                       
            
}


function set_ano(ano)
{
	
	$ano = ano;
}
