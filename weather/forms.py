from django import forms


class ChatForm(forms.Form):
    message = forms.CharField(
        max_length=500,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ask about the weather...",
                "class": "form-control",
            }
        )
    )