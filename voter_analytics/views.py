from django.views.generic import ListView, DetailView
from django.db import models
from .models import Voter
from .forms import VoterFilterForm
import plotly.express as px
from django.utils.safestring import mark_safe


class VoterListView(ListView):
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    context_object_name = 'voters'
    paginate_by = 100
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
            party = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_date_of_birth')
            max_dob = form.cleaned_data.get('max_date_of_birth')
            score = form.cleaned_data.get('voter_score')
            elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

            if party:
                queryset = queryset.filter(party_affiliation=party)
            if min_dob:
                queryset = queryset.filter(date_of_birth__year__gte=min_dob)
            if max_dob:
                queryset = queryset.filter(date_of_birth__year__lte=max_dob)
            if score:
                queryset = queryset.filter(voter_score=score)
            for election in elections:
                if form.cleaned_data.get(election):
                    queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterFilterForm(self.request.GET)
        return context

class VoterDetailView(DetailView):
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class GraphListView(ListView):
    model = Voter
    template_name = 'voter_analytics/graphs.html'
    context_object_name = 'voters'

    def get_queryset(self):
        queryset = Voter.objects.all()
        form = VoterFilterForm(self.request.GET)
        
        if form.is_valid():
            party = form.cleaned_data.get('party_affiliation')
            min_dob = form.cleaned_data.get('min_date_of_birth')
            max_dob = form.cleaned_data.get('max_date_of_birth')
            score = form.cleaned_data.get('voter_score')
            elections = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']

            if party:
                queryset = queryset.filter(party_affiliation=party)
            if min_dob:
                queryset = queryset.filter(date_of_birth__year__gte=min_dob)
            if max_dob:
                queryset = queryset.filter(date_of_birth__year__lte=max_dob)
            if score:
                queryset = queryset.filter(voter_score=score)
            for election in elections:
                if form.cleaned_data.get(election):
                    queryset = queryset.filter(**{election: True})

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET)
        context['form'] = form

        # Filtered queryset based on form inputs
        queryset = self.get_queryset()

        # 1. Histogram: Distribution of Voters by Year of Birth
        birth_year_counts = queryset.values('date_of_birth__year').annotate(count=models.Count('id')).order_by('date_of_birth__year')
        birth_year_chart = px.bar(
            x=[item['date_of_birth__year'] for item in birth_year_counts],
            y=[item['count'] for item in birth_year_counts],
            labels={'x': 'Year of Birth', 'y': 'Number of Voters'},
            title="Distribution of Voters by Year of Birth"
        )

        # 2. Pie Chart: Distribution of Voters by Party Affiliation
        party_affiliation_counts = queryset.values('party_affiliation').annotate(count=models.Count('party_affiliation'))
        party_chart = px.pie(
            names=[item['party_affiliation'] for item in party_affiliation_counts],
            values=[item['count'] for item in party_affiliation_counts],
            title="Distribution of Voters by Party Affiliation"
        )

        # 3. Histogram: Distribution of Voters by Participation in Each Election
        election_data = {
            '2020 State': queryset.filter(v20state=True).count(),
            '2021 Town': queryset.filter(v21town=True).count(),
            '2021 Primary': queryset.filter(v21primary=True).count(),
            '2022 General': queryset.filter(v22general=True).count(),
            '2023 Town': queryset.filter(v23town=True).count(),
        }
        election_participation_chart = px.bar(
            x=list(election_data.keys()),
            y=list(election_data.values()),
            labels={'x': 'Election', 'y': 'Number of Participants'},
            title="Voter Participation in Elections"
        )

        # Convert charts to HTML divs
        context['birth_year_chart'] = mark_safe(birth_year_chart.to_html(full_html=False, include_plotlyjs='cdn'))
        context['party_chart'] = mark_safe(party_chart.to_html(full_html=False, include_plotlyjs='cdn'))
        context['election_participation_chart'] = mark_safe(election_participation_chart.to_html(full_html=False, include_plotlyjs='cdn'))

        return context
    