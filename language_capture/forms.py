from django import forms

from language_capture.models import audiofile


class DocumentForm(forms.ModelForm):
    class Meta:
        model = audiofile
        fields = ('audio_file','session_name','percentage_of_key_words','number_of_key_words')
