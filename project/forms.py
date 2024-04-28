from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'start_time', 'end_time', 'donation_amount', 'is_featured', 'category', 'tags']


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if end_time <= start_time:
                raise ValidationError("End time must be after start time.")
        return cleaned_data

ImageFormSet = inlineformset_factory(Project, ProjectImage, fields=('image',))

class ImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']

ImageFormSet = forms.inlineformset_factory(Project, ProjectImage, form=ImageForm, extra=3)  # Allow 3 extra image fields


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ReportForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)        


class ReportCommentForm(forms.ModelForm):
     class Meta:
        model = ReportComment
        fields = ['comment_reason']   

class RatingForm(forms.ModelForm):
    class Meta:
        model = ProjectRating
        fields = ['rating']