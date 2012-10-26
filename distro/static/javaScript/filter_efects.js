/**
 * @author xama
 */
var count = 1;

function changeCountValue() {

	count = 0;
	//alert("esta - " + count);

}

function testeSearch() {

	require(["dojo/request", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, on, dom) {
		//alert("ola - " + count);

		var divTarget = dom.byId("buttonConfirm"), divConfirmPhrase = dom.byId("Confirmacao");

		if (count == 0) {

			//alert("vou modficiar");
			count = 1;

			request.get("addSaveButton").then(function(response) {
				divTarget.innerHTML = response;
				divConfirmPhrase.innerHTML = "";

			}, function(error) {
				// Display the error returned
				alert(response);
			});

		} else {

		}

	});
}

/*function teste_1() {

require(["dojo/request", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, on, dom) {

var b = dom.byId("butao");

// Attach the onclick event handler to the textButton
on(b, "click", function(evt) {

request.get("ajax").then(function(response) {
alert(response);

}, function(error) {
// Display the error returned
alert(response);
});

});
});

}*/

/***********/

function filter_oa() {

	var out_1 = 1;

	require(["dojo/request", "dojo/fx", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, fx, on, dom) {

		var wipeOutButton_1 = dom.byId("oa_button"), wipeInButton_1 = dom.byId("oa_button"), wipeTarget_1 = dom.byId("oa");

		on(wipeInButton_1, "click", function(evt) {

			if (out_1 == 1) {

				//esconder a div
				wipeTarget_1.style.display = "block";
				request.get("filter_abc").then(function(response) {

					wipeTarget_1.innerHTML = response;

				}, function(error) {
					// Display the error returned
					alert(response + "errro");
				});

				out_1 = 0;
				fx.wipeIn({
					node : wipeTarget_1
				}).play();
			} else {

				wipeTarget_1.innerHTML = "";

				out_1 = 1;
				fx.wipeOut({
					node : wipeTarget_1
				}).play();

				wipeTarget_1.style.display = "block";
			}
		});

	});
}

function filter_dep() {
	var out_2 = 1;

	require(["dojo/request", "dojo/fx", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, fx, on, dom) {
		var wipeOutButton_2 = dom.byId("da_button"), wipeInButton_2 = dom.byId("da_button"), wipeTarget_2 = dom.byId("dep");
		//esconder a div

		on(wipeInButton_2, "click", function(evt) {
			if (out_2 == 1) {

				wipeTarget_2.style.display = "block";
				out_2 = 0;
				request.get("filter_dep").then(function(response) {

					wipeTarget_2.innerHTML = response;

				}, function(error) {
					// Display the error returned
					alert(response + "errro");
				});

				fx.wipeIn({
					node : wipeTarget_2
				}).play();

			} else {

				wipeTarget_2.innerHTML = "";

				out_2 = 1;
				fx.wipeOut({
					node : wipeTarget_2
				}).play();

				wipeTarget_2.style.display = "block";
			}

		});
	});
}

function filter_cat() {
	var out_3 = 1;
	require(["dojo/request", "dojo/fx", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, fx, on, dom) {
		////////////////

		var wipeOutButton_3 = dom.byId("ca_button"), wipeInButton_3 = dom.byId("ca_button"), wipeTarget_3 = dom.byId("category");
		//esconder a div

		on(wipeInButton_3, "click", function(evt) {
			if (out_3 == 1) {

				wipeTarget_3.style.display = "block";
				out_3 = 0;
				request.get("filter_cat").then(function(response) {

					wipeTarget_3.innerHTML = response;

				}, function(error) {
					// Display the error returned
					alert(response + "errro");
				});

				fx.wipeIn({
					node : wipeTarget_3
				}).play();

			} else {

				wipeTarget_3.innerHTML = "";

				out_3 = 1;
				fx.wipeOut({
					node : wipeTarget_3
				}).play();

				wipeTarget_3.style.display = "block";
			}
		});

	});
}

function filter_date() {
	var out_4 = 1;
	require(["dojo/request", "dojo/fx", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, fx, on, dom) {
		////////*Por data*////////

		var wipeOutButton_4 = dom.byId("date_button"), wipeInButton_4 = dom.byId("date_button"), wipeTarget_4 = dom.byId("date");
		//esconder a div

		on(wipeInButton_4, "click", function(evt) {
			if (out_4 == 1) {

				wipeTarget_4.style.display = "block";
				out_4 = 0;

				fx.wipeIn({
					node : wipeTarget_4
				}).play();

			} else {

				out_4 = 1;
				fx.wipeOut({
					node : wipeTarget_4
				}).play();

				wipeTarget_4.style.display = "block";
			}

			date_function();
		});

	});
}

/*************************/

function date_function() {

	var out_5 = 1;
	var out_6 = 1;
	require(["dojo/fx", "dojo/on", "dojo/dom", "dojo/domReady!"], function(fx, on, dom) {

		//Data de inicio

		var wipeInButton_5 = dom.byId("start_date_button"), wipeTarget_5 = dom.byId("start_date");
		//esconder a div

		on(wipeInButton_5, "click", function(evt) {

			if (out_5 == 1) {

				wipeTarget_5.style.display = "block";
				out_5 = 0;

				fx.wipeIn({
					node : wipeTarget_5
				}).play();

			} else {

				out_5 = 1;
				fx.wipeOut({
					node : wipeTarget_5
				}).play();

				wipeTarget_5.style.display = "block";
			}
		});

		//Data de inicio

		var wipeInButton_6 = dom.byId("end_date_button"), wipeTarget_6 = dom.byId("end_date");
		//esconder a div

		on(wipeInButton_6, "click", function(evt) {

			if (out_6 == 1) {

				wipeTarget_6.style.display = "block";
				out_6 = 0;

				fx.wipeIn({
					node : wipeTarget_6
				}).play();

			} else {

				out_6 = 1;
				fx.wipeOut({
					node : wipeTarget_6
				}).play();

				wipeTarget_6.style.display = "block";
			}
		});

	});
}

/*
 * filtrar por curso
 */

function filter_curso() {

	var out_7 = 1;
	require(["dojo/request", "dojo/request/notify", "dojo/fx", "dojo/on", "dojo/dom", "dojo/domReady!"], function(request, notify, fx, on, dom) {
		////////////////

		var wipeOutButton_7 = dom.byId("curso_button"), wipeInButton_7 = dom.byId("curso_button"), wipeTarget_7 = dom.byId("curso");
		var ajaxLoader = dom.byId("ajaxLoader");
		//esconder a div

		on(wipeInButton_7, "click", function(evt) {
			if (out_7 == 1) {

				
				wipeTarget_7.style.display = "block";

				out_7 = 0;

				notify("start", function() {
					ajaxLoader.className = "showAjaxLoader";
				});
				notify("done", function(data) {
					
					ajaxLoader.className = "hideAjaxLoader";
					
				});
				request.get("filter_curso").then(function(response) {

					wipeTarget_7.innerHTML = response;

				}, function(error) {
					// Display the error returned
					alert(response + "errro");
				});

				fx.wipeIn({
					node : wipeTarget_7
				}).play();

			} else {

				wipeTarget_7.innerHTML = "";

				out_7 = 1;
				fx.wipeOut({
					node : wipeTarget_7
				}).play();

				wipeTarget_7.style.display = "block";
			}
		});

	});
}

/***************************/
/*
 function start_date_filter() {

 require(["dojo/on", "dojo/dom", "dojo/dom-form", "dojo/request", "dojo/domReady!"], function(on, dom, domForm, request) {

 var sumbitDateStart = dom.byId("submitStartDate"), content = dom.byId("form_start_date");

 on(sumbitDateStart, "click", function(evt) {

 request.get("filter_date_start", {

 data : {
 color : "blue",
 answer : 42
 },
 headers : {
 ola : "A value"
 },
 //query: domForm.toObject("form_start_date")

 }).then(function(response) {
 alert("ola")

 });

 });

 });

 }*/
