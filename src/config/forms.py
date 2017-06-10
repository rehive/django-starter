from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data
