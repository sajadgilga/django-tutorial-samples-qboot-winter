from django.db.models import Q, Case, When, F, CharField
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView

from football.forms import TeamForm
from football.models import Fixture, LeagueSeason, Team


def fetch_team_fixtures(request):
    team_name = request.GET.get("team")
    season = request.GET.get("season", "2024")
    league = request.GET.get("league", "laliga")

    seasons = LeagueSeason.objects.filter(season=season, league__name=league)
    fixtures = Fixture.objects.filter(Q(away__name=team_name) | Q(home__name=team_name),
                                      round__season__in=seasons, ).annotate(
        opponent=Case(When(home__name=team_name, then=F("away__name")), default=F("home__name"),
                      output_field=CharField())
    ).values("start_date", "venue", "opponent")
    return HttpResponse(fixtures)


class BaseFetchView(View):
    message = 'default message'

    def extract_query_params(self):
        self.team_name = self.request.GET.get("team")
        self.season = self.request.GET.get("season", "2024")
        self.league = self.request.GET.get("league", "laliga")

    def filter_query(self):
        seasons = LeagueSeason.objects.filter(season=self.season, league__name=self.league)
        return Fixture.objects.filter(Q(away__name=self.team_name) | Q(home__name=self.team_name),
                                      round__season__in=seasons, ).annotate(
            opponent=Case(When(home__name=self.team_name, then=F("away__name")), default=F("home__name"),
                          output_field=CharField())
        ).values("start_date", "venue", "opponent")

    def get(self, request):
        self.extract_query_params()
        return JsonResponse({'data': list(self.filter_query()), 'message': self.message}, safe=False)


class FetchTeamAwayFixtures(BaseFetchView):
    def filter_query(self):
        return Fixture.objects.filter(away__name=self.team_name).values_list('start_date', 'venue')


class FetchTeamHomeFixtures(BaseFetchView):
    message = 'home games retrieved'

    def filter_query(self):
        return Fixture.objects.filter(home__name=self.team_name).values_list('start_date', 'venue')


class TeamNameView(TemplateView):
    template_name = 'team_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = Team.objects.first().name
        return context


class TeamsView(ListView):
    model = Team
    context_object_name = 'team_list'


class TeamInfoView(DetailView):
    model = Team


class TeamCreateView(FormView):
    form_class = TeamForm
    template_name = 'team_create.html'
    success_url = reverse_lazy('create_team')

    def form_valid(self, form):
        print("form is valid")
        form.save(commit=True)
        return super().form_valid(form)


class TeamCreateViewV2(CreateView):
    model = Team
    fields = ('name', 'default_league_season',)
