from django import forms


class EmployeeForm(forms.Form):
    gitlab_username = forms.CharField(max_length=200)


