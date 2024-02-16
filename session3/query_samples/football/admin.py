from django.contrib import admin

from football.models import Fixture, Team


# Register your models here.


@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('id', 'away', 'home', 'round', 'round_season')

    def round_season(self, obj):
        if obj.round:
            return obj.round.season.season


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
