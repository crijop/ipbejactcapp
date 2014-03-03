function submit_start_date()
{
	
	$("#form_start_date").submit();
}


function submit_end_date()
{
	
	$("#form_end_date").submit();
}


function teste_ajax()
{
	

	
	$.ajax({
      		type: "GET",
          	url:"/distro/recursosHumanos/teste_ajax/",
          	success: function(response) {
            	
          
            	$(".jumbotron").after(response.html);
            	 $( ".teste_dialogo" ).dialog({
      				resizable: true,
      				draggable: false,
      				width:800,
      				modal: true,
      				title: "Dialog Title",
      				close: function()
      				{
      					$( ".teste_dialogo" ).remove();
      				}
			     
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

function form_validation($id)
{


$form = $("form");
		
	$.ajax({
		type: "GET",
		url: "/distro/recursosHumanos/valid_ajax/"+$id,
		data: $form.serialize(),
		success: function(response)
		{
			$(".alert-danger").remove();
			
	
			if(response.valid == "n")
			{
			
				for(error in response.errors)
				{
					$html = '<div class="alert alert-danger">';
					$html = $html + response.errors[error];
					$html = $html + '</div>';
					
					$("#id_"+error).parent().after($html);
					
					//alert(response.html[error]);
				}
			}else
			{
		
				$("#buttonConfirm").after(response.html);
            	 $( ".teste_dialogo" ).dialog({
      				resizable: true,
      				draggable: false,
      				width:800,
      				modal: true,
      				title: "Confrmar Edição de Docente",
      				close: function()
      				{
      					$( ".teste_dialogo" ).remove();
      				}
			     
			    });
			}
		},
		error: function(error)
		{
			
		}
	});

}
