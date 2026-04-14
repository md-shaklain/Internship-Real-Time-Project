from django import forms
from .models import UserAccount

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = [
            'username',
            'email',
            'role',
            'password',
            'security_question',
            'security_answer'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user