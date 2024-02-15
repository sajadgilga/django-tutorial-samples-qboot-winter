from django.contrib import admin

# Register your models here.
from football.models import Fixture, Team


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('id', 'away', 'home', 'round', 'round_season')

    def round_season(self, obj):
        if obj.round:
            return obj.round.season.season


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
