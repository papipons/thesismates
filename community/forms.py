from django import forms
from . import models as com_m
from django.utils.text import slugify

# --------------------------------------------------------------------

class SearchForm(forms.Form):
    search = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'type' : 'text',
                'placeholder' : 'Search keywords in question title'
                }
            )
        )

 # --------------------------------------------------------------------

class AskQuestionForm(forms.ModelForm):
	def save_question(self, user):
		title = self.cleaned_data['title']
		question = self.save(commit=False)
		question.asked_by = user
		question.slug = slugify(title)
		question.save()

		return question

	title = forms.CharField(
	    widget = forms.TextInput(
	        attrs = {
	            'class' : 'form-control'
	            }
	        )
	    )

	description = forms.CharField(
	        widget = forms.Textarea(
	            attrs = {
	                'class' : 'form-control',
	                'rows' : '3',
	            }
	        ),
	        required=False
	    )
	class Meta:
		model = com_m.Question
		fields = ('title','description')

# --------------------------------------------------------------------

class AnswerQuestionForm(forms.ModelForm):
	def save_answer(self, ques, user):
		answer = self.save(commit=False)
		answer.question = ques
		answer.answered_by = user
		answer.save()

	answer = forms.CharField(
	        widget = forms.Textarea(
	            attrs = {
	                'class' : 'form-control',
	                'rows' : '3',
	            }
	        ),
	    )
	class Meta:
		model = com_m.Question_Answer
		fields = ('answer',)
