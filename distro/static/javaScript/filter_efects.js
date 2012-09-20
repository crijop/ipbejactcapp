/**
 * @author xama
 */

	var out_1 = 1;
	var out_2 = 1;
	require(["dojo/fx", "dojo/on", "dojo/dom", "dojo/domReady!"], function(fx, on, dom) {
		var wipeOutButton_1= dom.byId("oa_button"), wipeInButton_1 = dom.byId("oa_button"), wipeTarget_1 = dom.byId("oa");
		//esconder a div
		wipeTarget_1.style.display = "none";
		on(wipeInButton_1, "click", function(evt) {
			if (out_1 == 1) {

				out_1 = 0;
				fx.wipeIn({
					node : wipeTarget_1
				}).play();
			} else {
				out_1 = 1;
				fx.wipeOut({
					node : wipeTarget_1
				}).play();
			}
		});
		
		var wipeOutButton_2= dom.byId("da_button"), wipeInButton_2 = dom.byId("da_button"), wipeTarget_2 = dom.byId("dep");
		//esconder a div
		wipeTarget_2.style.display = "none";
		
		on(wipeInButton_2, "click", function(evt) {
			if (out_2 == 1) {
				
				
				out_2 = 0;
				fx.wipeIn({
					node : wipeTarget_2
				}).play();
				
			} else {
				out_2 = 1;
				fx.wipeOut({
					node : wipeTarget_2
				}).play();
			}
		});

	}); 
