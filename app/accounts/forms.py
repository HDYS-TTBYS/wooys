from django import forms

from .models import UserIncluded


class UserIncludedCreateForm(forms.ModelForm):
    class Meta:
        model = UserIncluded
        fields = ("img",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
