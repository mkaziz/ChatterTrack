from django import forms

class TrackForm(forms.Form):
    twitter_handle = forms.CharField(max_length=100, label='Twitter Handle')
    #tracking_phrases = forms.CharField(widget=forms.Textarea, label='Tracking Phrases')
    #time_to_track = forms.IntegerField()

class UploadImageForm(forms.Form):
    image = forms.ImageField()
    image.widget.attrs["onchange"]="this.form.submit();"
    stream_id = forms.CharField(max_length=100)
    stream_id.widget.attrs["style"]="display:none;"
    
