function hideRegionSelect() {
	var usertype = document.getElementById("usertype-input");
	var psk_region = document.getElementById("div-id-psk-region");

	if(usertype.value == "Coordinator" || usertype.value == "Field Assistant"){
		psk_region.setAttribute("style", "display: block;");
	}else{
		psk_region.setAttribute("style", "display: none;");
	}
	
}

function visit_form_validator(){
	// Report submission last three months
	report_submit_one = document.getElementById('report-submit-one');
	report_submit_two = document.getElementById('report-submit-two');
	report_submit_three = document.getElementById('report-submit-three');
	report_submit_four = document.getElementById('report-submit-four');
	// Ordered last quarter
	quarter_order_yes = document.getElementById('quarter-order-yes');
	quarter_order_no = document.getElementById('quarter-order-no');
	// OJT
	ojt_done = document.getElementById('ojt-done');
	ojt_not = document.getElementById('ojt-not');
	ojt_yes = document.getElementById('ojt-yes');
	ojt_no = document.getElementById('ojt-no');
	formIssues = 0;
}

function verifyDates(){
	var visit_date = document.getElementById('visiting-date').value;
	var error_div = document.getElementById('date-error');
	var dateInput = new Date(visit_date);
	var today = new Date();
	today.setHours(0,0,0,0);

	if(dateInput > today+1){
		error_div.setAttribute("style", "display: block;");
		error_div.innerHTML = "Error! Date entered is invalid. Kindly correct"
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

function hideLDFields() {
	var ld_quantity = document.getElementById("ld-quantity");
	var ld_invoice_avail = document.getElementById("ld-invoice-avail")
	var ld_dates = document.getElementById("ld-dates");
	var ld_yes = document.getElementById("ld-yes");
	var ld_no = document.getElementById("ld-no");

	if(ld_no.checked){
		ld_quantity.setAttribute("style", "display: none;");
		ld_invoice_avail.setAttribute("style", "display: none;");
		ld_dates.setAttribute("style", "display: none;");
	}else if(ld_yes.checked){
		ld_quantity.setAttribute("style", "display: block;");
		ld_invoice_avail.setAttribute("style", "display: block;");
		ld_dates.setAttribute("style", "display: block;");
	}else{
		ld_quantity.setAttribute("style", "display: none;");
		ld_invoice_avail.setAttribute("style", "display: none;");
		ld_dates.setAttribute("style", "display: none;");
	}
	
}

function hideLLDFields() {
	var lld_quantity = document.getElementById("lld-quantity");
	var lld_invoice_avail = document.getElementById("lld-invoice-avail");
	var lld_dates = document.getElementById("lld-dates");
	var lld_yes = document.getElementById("lld-yes");
	var lld_no = document.getElementById("lld-no");

	if(lld_no.checked){
		lld_quantity.setAttribute("style", "display: none;");
		lld_invoice_avail.setAttribute("style", "display: none;");
		lld_dates.setAttribute("style", "display: none;");
	}else if(lld_yes.checked){
		lld_quantity.setAttribute("style", "display: block;");
		lld_invoice_avail.setAttribute("style", "display: block;");
		lld_dates.setAttribute("style", "display: block;");
	}else{
		lld_quantity.setAttribute("style", "display: none;");
		lld_invoice_avail.setAttribute("style", "display: none;");
		lld_dates.setAttribute("style", "display: none;");
	}
	
}

function hideInvoiceFields() {
	var ld_invoice = document.getElementById("ld-invoice");
	var invoice_yes = document.getElementById("invoice-yes");
	var invoice_no = document.getElementById("invoice-no");

	if(invoice_yes.checked){
		ld_invoice.setAttribute("style", "display: block;");
	}else if(invoice_no.checked){
		ld_invoice.setAttribute("style", "display: none;");
	}else{
		ld_invoice.setAttribute("style", "display: none;");
	}
	
}

function hideLLDInvoiceFields() {
	var lld_invoice = document.getElementById("lld-invoice");
	var lld_invoice_yes = document.getElementById("lld-invoice-yes");
	var lld_invoice_no = document.getElementById("lld-invoice-no");

	if(lld_invoice_yes.checked){
		lld_invoice.setAttribute("style", "display: block;");
	}else if(lld_invoice_no.checked){
		lld_invoice.setAttribute("style", "display: none;");
	}else{
		lld_invoice.setAttribute("style", "display: none;");
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

	if(book_bal.value!=physical_count.value){
		bal_variance_reason.setAttribute("style", "display: block");
		bal_variance_reason.setAttribute("required", "True");
	}else if(book_bal.value==physical_count.value){
		bal_variance_reason.setAttribute("style", "display: none");
	}else{
		bal_variance_reason.setAttribute("style", "display: none");
	}
}