from django import forms

from football.models import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'default_league_season',)
