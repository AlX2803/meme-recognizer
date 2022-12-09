from django import forms

class ImgForm(forms.Form):
	select_a_meme = forms.ImageField()
