import uuid

from django.core.files.storage import FileSystemStorage
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.

team_logo_fs = FileSystemStorage('teams')


class League(models.Model):
    name = models.CharField(max_length=127, verbose_name="name")


class LeagueSeason(models.Model):
    league = models.ForeignKey(
        League,
        on_delete=models.CASCADE,
        related_name="related_seasons",
        verbose_name="league",
    )
    season = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex="^.{4}$", message="Length has to be 4", code="nomatch")],
        verbose_name="season",
    )
    teams = models.ManyToManyField("Team", related_name="related_seasons", blank=True, verbose_name="teams")
    current = models.BooleanField(default=False, verbose_name="current")
    start_date = models.DateField(null=True, blank=True, verbose_name="start date")
    end_date = models.DateField(null=True, blank=True, verbose_name="end date")

    class Meta:
        db_table = "football_league_season"
        constraints = [models.UniqueConstraint(fields=["league", "season"], name="unique_football_league_season")]

        verbose_name_plural = "football leagueseasons"
        verbose_name = "football leagueseason"
        ordering = ("-season",)


class LeagueRoundType(models.IntegerChoices):
    other = 0, "other"
    final = 1, "Final"
    semi_finals = 2, "Semi-Finals"
    third_place_final = 3, "3rd PlaceFinal"
    quarter_final = 4, "Quarter-Finals"
    eighth_final = 5, "8th Finals"


class LeagueRound(models.Model):
    season = models.ForeignKey(
        LeagueSeason,
        on_delete=models.CASCADE,
        related_name="related_rounds",
        verbose_name="season",
    )
    name = models.CharField(max_length=127, verbose_name="name")
    type = models.PositiveSmallIntegerField(
        default=LeagueRoundType.other, choices=LeagueRoundType.choices, verbose_name="round type"
    )

    class Meta:
        db_table = "football_league_round"
        constraints = [models.UniqueConstraint(fields=["season", "name"], name="unique_football_league_round")]
        verbose_name_plural = "football leaguerounds"
        verbose_name = "football leagueround"


class Team(models.Model):
    default_league_season = models.ForeignKey(
        "LeagueSeason",
        on_delete=models.PROTECT,
        related_name="related_teams",
        blank=True,
        null=True,
        default=None,
        verbose_name="default season",
    )
    name = models.CharField(max_length=255, verbose_name="name")
    logo = models.ImageField(max_length=255, storage=team_logo_fs, null=True, verbose_name="logo")

    def __str__(self):
        return self.name


class Fixture(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    week_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="week number")
    round = models.ForeignKey(
        LeagueRound,
        on_delete=models.CASCADE,
        related_name="related_fixtures",
        verbose_name="round",
    )
    venue = models.CharField(max_length=64, verbose_name="venue", null=True)
    home = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="related_home_fixtures",
        verbose_name="home",
    )
    away = models.ForeignKey(
        Team,
        on_delete=models.PROTECT,
        related_name="related_away_fixtures",
        verbose_name="away",
    )
    start_date = models.DateTimeField(null=True, verbose_name="start date")
