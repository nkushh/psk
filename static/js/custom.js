function hideRegionSelect() {
	var usertype = document.getElementById("usertype-input");
	var psk_region = document.getElementById("div_id_psk_region");

	if(usertype.value == "Coordinator"){
		psk_region.setAttribute("style", "display: block;");
	}else{
		psk_region.setAttribute("style", "display: none;");
	}
	
}

function hideNonComplianceReason() {
	var noncompliance_reason = document.getElementById("noncompliance-reason");
	var compliance_yes = document.getElementById("compliance-yes");
	var compliance_no = document.getElementById("compliance-no");

	if(compliance_no.checked){
		noncompliance_reason.setAttribute("style", "display: block;");
	}else if(compliance_yes.checked){
		noncompliance_reason.setAttribute("style", "display: none;");
	}else{
		noncompliance_reason.setAttribute("style", "display: none;");
	}
	
}

function showFirePreventionMech() {
	var fire_prevention_mechanism = document.getElementById("fire-prevention-mechanism");
	var fire_prevention = document.getElementById("fire-prevention");
	var no_fire_prevention = document.getElementById("no-fire-prevention");

	if(fire_prevention.checked){
		fire_prevention_mechanism.setAttribute("style", "display: block;");
	}else if(no_fire_prevention.checked){
		fire_prevention_mechanism.setAttribute("style", "display: none;");
	}else{
		fire_prevention_mechanism.setAttribute("style", "display: none;");
	}
	
}

function hideBalVarianceReason(){
	var bal_variance_reason = document.getElementById("bal-variance-reason");
	var book_bal = document.getElementById("book-bal");
	var physical_count = document.getElementById("physical-count");

	if(book_bal!=physical_count){
		bal_variance_reason.setAttribute("style", "display: block");
	}else if(book_bal==physical_count){
		bal_variance_reason.setAttribute("style", "display: none");
	}else{
		bal_variance_reason.setAttribute("style", "display: none");
	}
}