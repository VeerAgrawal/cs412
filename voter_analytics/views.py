# File: views.py  
# Author: Veer Agrawal (veer1@bu.edu), 6/15/2025  
# Description: Django viewss file

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, TemplateView
from .models import Voter

import plotly
import plotly.graph_objs as go
import pandas as pd




class VoterListView(ListView):
    """Displays a paginated list of voters with support for filtering."""

    template_name = 'voter_analytics/voter_list.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        """Filter voters by selected criteria from the form."""

        voters = super().get_queryset()

        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_dob')
        max_year = self.request.GET.get('max_dob')
        score = self.request.GET.get('score')

        # voting participation checkboxes
        voted_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for field in voted_fields:
            if self.request.GET.get(field) == 'on':
                voters = voters.filter(**{field: True})

        if party:
            voters = voters.filter(party_affiliation=party.strip())

        if min_year:
            voters = voters.filter(date_of_birth__gte=f'{min_year}-01-01')
        if max_year:
            voters = voters.filter(date_of_birth__lte=f'{max_year}-12-31')
        if score:
            voters = voters.filter(voter_score=int(score))

        return voters.order_by('last_name', 'first_name')
    
    def get_context_data(self, **kwargs):
        """Pass additional context to support filtering in template."""

        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['year_range'] = list(range(1900, 2025))
        context['score_range'] = list(range(0, 6))
        return context



class VoterDetailView(DetailView):
    """Displays detailed information for a single voter."""

    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    context_object_name = 'voter'

class VoterGraphView(TemplateView):
    """Displays graphs summarizing voter data."""

    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        """creates Plotly graphs based on voter data."""

        context = super().get_context_data(**kwargs)
        voters = Voter.objects.all()

        request = self.request
        party = request.GET.get('party')
        min_year = request.GET.get('min_dob')
        max_year = request.GET.get('max_dob')
        score = request.GET.get('score')

        voted_fields = ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']
        for field in voted_fields:
            if request.GET.get(field) == 'on':
                voters = voters.filter(**{field: True})

        if party:
            voters = voters.filter(party_affiliation=party.strip())
        if min_year:
            voters = voters.filter(date_of_birth__gte=f'{min_year}-01-01')
        if max_year:
            voters = voters.filter(date_of_birth__lte=f'{max_year}-12-31')
        if score:
            voters = voters.filter(voter_score=int(score))

        df = pd.DataFrame(list(voters.values()))
        graphs = {}

        if not df.empty:
            # Histogram by Birth Year
            df['birth_year'] = pd.to_datetime(df['date_of_birth']).dt.year
            fig1 = go.Figure(
                data=[go.Histogram(x=df['birth_year'])],
                layout_title_text="Voters by Birth Year"
            )
            graphs['birth_year_hist'] = plotly.offline.plot(fig1, auto_open=False, output_type='div')

            # Pie Chart for Party Affiliation
            party_counts = df['party_affiliation'].value_counts()
            fig2 = go.Figure(
                data=[go.Pie(labels=party_counts.index, values=party_counts.values)],
                layout_title_text="Party Affiliation Breakdown"
            )
            graphs['party_pie'] = plotly.offline.plot(fig2, auto_open=False, output_type='div')

            # Bar Chart for Voter Participation
            participation_counts = {
                field: df[field].sum() for field in voted_fields if field in df.columns
            }
            labels = {
                'v20state': '2020 State',
                'v21town': '2021 Town',
                'v21primary': '2021 Primary',
                'v22general': '2022 General',
                'v23town': '2023 Town'
            }
            x_vals = [labels[k] for k in participation_counts]
            y_vals = list(participation_counts.values())
            fig3 = go.Figure(
                data=[go.Bar(x=x_vals, y=y_vals)],
                layout_title_text="Participation by Election"
            )
            graphs['election_bar'] = plotly.offline.plot(fig3, auto_open=False, output_type='div')

        context['graphs'] = graphs
        context['request'] = self.request
        context['year_range'] = list(range(1900, 2025))
        context['score_range'] = list(range(0, 6))
        return context