from django import forms

REPORT_SUBMSSN = (('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'))
QTR_ORDR = (('0', 'No'), ('1', 'Yes'))

class NewVisitForm(forms.Form):
	reporting_frequency = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'radio-inline'}), choices=REPORT_SUBMSSN)
	quarter_order = forms.ChoiceField(widget=forms.RadioSelect, choices=QTR_ORDR)
