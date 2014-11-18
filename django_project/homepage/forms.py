from django import forms

class SpellForm(forms.Form):
	ad =  forms.IntegerField(min_value=0, label="Enter your attack power (AD): ")
	ap =  forms.IntegerField(min_value=0, label="Enter your ability power (AP): ")
	cdr = forms.IntegerField(min_value=0, max_value=40,label="Enter your cooldown reduction (CDR %): ")