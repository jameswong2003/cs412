from django import forms
from .models import Voter
from datetime import datetime

class VoterFilterForm(forms.Form):
    PARTY_CHOICES = [(party, party) for party in Voter.objects.values_list('party_affiliation', flat=True).distinct()]
    SCORE_CHOICES = [(score, score) for score in Voter.objects.values_list('voter_score', flat=True).distinct()]
    CURRENT_YEAR = datetime.now().year
    YEAR_CHOICES = [(year, year) for year in range(1900, CURRENT_YEAR + 1)]

    party_affiliation = forms.ChoiceField(choices=[('', 'Any')] + PARTY_CHOICES, required=False)
    min_date_of_birth = forms.ChoiceField(choices=[('', 'Any')] + YEAR_CHOICES, required=False)
    max_date_of_birth = forms.ChoiceField(choices=[('', 'Any')] + YEAR_CHOICES, required=False)
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + SCORE_CHOICES, required=False)
    
    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)
