from django import forms

from .models import Article


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title",  "search_tag", "content")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
