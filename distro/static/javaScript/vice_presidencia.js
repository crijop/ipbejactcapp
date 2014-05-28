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
