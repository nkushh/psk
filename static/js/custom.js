function hideRegionSelect() {
	var usertype = document.getElementById("usertype-input");
	var psk_region = document.getElementById("div_id_psk_region");

	if(usertype.value == "Coordinator"){
		psk_region.setAttribute("style", "display: block;");
	}else{
		psk_region.setAttribute("style", "display: none;");
	}
	
}