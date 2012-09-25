/**
 * @author xama
 */
function teste_1() {

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

}

/***********/

function teste_2() {

	var out_1 = 1;
	var out_2 = 1;
	var out_3 = 1;
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
		
		////////////////
		
		var wipeOutButton_3 = dom.byId("ca_button"), wipeInButton_3 = dom.byId("ca_button"), wipeTarget_3 = dom.byId("category");
		//esconder a div

		on(wipeInButton_3, "click", function(evt) {
			if (out_3 == 1) {

				wipeTarget_3.style.display = "block";
				out_3= 0;
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

/*************************/

/***************************/