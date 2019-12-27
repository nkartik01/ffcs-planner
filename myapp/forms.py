from django import forms
from .models import *

class input1form(forms.Form):
    num=forms.DecimalField(widget = forms.NumberInput (attrs={"class": "form-control", "placeholder":"Course Count",}), label ='Number of courses',max_digits=8,decimal_places=0, min_value=0,required=False)

class input2form(forms.Form):
    theory=forms.ChoiceField(choices=(('All','All'),('Morning Only Theory','Morning Only Theory'),('Evening Only Theory','Evening Only Theory'),('Either Morning or Evening Theory','Either Morning or Evening Theory')))
    def __init__(self,n, *args, **kwargs):
        super(input2form, self).__init__( *args, **kwargs)
        #print(n)
        for i in range (n):
            self.fields['course %d' %i]=forms.CharField(max_length=10)
