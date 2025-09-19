from django import forms

class TranslateForm(forms.Form):
    text = forms.CharField(label='Enter text (optional)', required=False, widget=forms.Textarea)
    language = forms.ChoiceField(choices=[
        ('Yoruba', 'Yoruba'),
        ('Igbo', 'Igbo'),
        ('Hausa', 'Hausa'),
        ('Swahili', 'Swahili'),
        ('Zulu', 'Zulu'),
        ('Xhosa', 'Xhosa'),
        ('Somali', 'Somali'),
        ('Amharic', 'Amharic'),
        ('Arabic', 'Arabic'),
        ('Afrikaans', 'Afrikaans'),
        ('Tigrinya', 'Tigrinya'),
        ('Tiv', 'Tiv'),
    ])
    



class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label='Upload audio (WAV/MP3)', required=True)
