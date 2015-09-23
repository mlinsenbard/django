from django import forms
import _mysql

ad_errors = {
    'required': 'A value for Attack Damage is required',
    'invalid': 'Attack Damage value must be 0 or greater'
}

ap_errors = {
    'required': 'A value for Ability Power is required',
    'invalid': 'Ability Power value must be 0 or greater'
}

cdr_errors = {
    'required': 'A value for Cooldown Reduction is required',
    'invalid': 'Cooldown Reduction must be a number (%) between 0 and 40'
}

class SpellForm(forms.Form):
	ad =  forms.IntegerField(min_value=0, label="Enter your attack power (AD): ",
	error_messages=ad_errors)
	ap =  forms.IntegerField(min_value=0, label="Enter your ability power (AP): ",
	error_messages=ap_errors)
	cdr = forms.IntegerField(min_value=0, max_value=40,
	label="Enter your cooldown reduction (CDR %): ", error_messages=cdr_errors)
