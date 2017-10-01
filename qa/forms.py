from django import forms

from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=120)
    text = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['author_id'] = 1
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

    def save(self):
        self.cleaned_data['question'] = Question.objects.get(id=self.cleaned_data['question'])
        self.cleaned_data['author_id'] = 1
        answer = Answer(**self.cleaned_data)
        answer.save()
        return Answer
