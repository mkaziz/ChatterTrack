from django import forms

class TrackForm(forms.Form):
    twitter_handle = forms.CharField(max_length=100, label='Twitter Handle')
    tracking_phrases = forms.CharField(widget=forms.Textarea, label='Tracking Phrases')
    
