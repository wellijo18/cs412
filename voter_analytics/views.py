# views.py
from django.views.generic import ListView, DetailView
from .models import Voter
import plotly
import plotly.graph_objs as go

class VoterListView(ListView):
    '''View to display voter records'''

    template_name = 'voter_analytics/results.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100
    def get_queryset(self):
        voters = super().get_queryset().order_by('da_last_name')

        # all filters for different attribtes
        if 'min_dob' in self.request.GET:
          min_dob = self.request.GET['min_dob']
          if min_dob:
            voters = voters.filter(da_dob__year__gte=min_dob)
        if 'max_dob' in self.request.GET:
          max_dob = self.request.GET['max_dob']
          if max_dob:
            voters = voters.filter(da_dob__year__lte=max_dob)
        if 'party' in self.request.GET:
          party = self.request.GET['party']
          if party:
            voters = voters.filter(da_party=party)

        if 'voter_score' in self.request.GET:
          voter_score = self.request.GET['voter_score']
          if voter_score:
            voters = voters.filter(da_voter_score=voter_score)
        # for the different elections

        if 'v20state' in self.request.GET:
            voters = voters.filter(da_v20state=True)
        if 'v21town' in self.request.GET:
            voters = voters.filter(da_v21town=True)
        if 'v21primary' in self.request.GET:
            voters = voters.filter(da_v21primary=True)
        if 'v22general' in self.request.GET:
            voters = voters.filter(da_v22general=True)
        if 'v23town' in self.request.GET:
            voters = voters.filter(da_v23town=True)
        return voters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # to pass da data into the templates
        context['parties'] = Voter.objects.values_list('da_party', flat=True).distinct().order_by('da_party')
        context['years'] = range(1900, 2024)
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')

        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')
        return context

class VoterDetailView(DetailView):
    '''View to show view page for one voter'''
    # single voter page 
    template_name = 'voter_analytics/result_detail.html'
    model = Voter
    context_object_name = 'v'

class VoterGraphListView(ListView):
    '''View to display the graphs of voters'''
    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'
    # get info for graphs
    def get_queryset(self):
        voters = super().get_queryset()
        if 'min_dob' in self.request.GET:
            min_dob = self.request.GET['min_dob']
            if min_dob:
                voters = voters.filter(da_dob__year__gte=min_dob)

        if 'max_dob' in self.request.GET:
            max_dob = self.request.GET['max_dob']
            if max_dob:
                voters = voters.filter(da_dob__year__lte=max_dob)

        if 'party' in self.request.GET:
            party = self.request.GET['party']
            if party:
                voters = voters.filter(da_party=party)

        if 'voter_score' in self.request.GET:
            voter_score = self.request.GET['voter_score']
            if voter_score:
                voters = voters.filter(da_voter_score=voter_score)
        if 'v20state' in self.request.GET:
            voters = voters.filter(da_v20state=True)
        if 'v21town' in self.request.GET:
            voters = voters.filter(da_v21town=True)
        if 'v21primary' in self.request.GET:
            voters = voters.filter(da_v21primary=True)
        if 'v22general' in self.request.GET:
            voters = voters.filter(da_v22general=True)
        if 'v23town' in self.request.GET:
            voters = voters.filter(da_v23town=True)

        return voters
    # get and pass on context data to properly contruct graphs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voters = self.get_queryset()

        # pass da filters to graphs
        context['parties'] = Voter.objects.values_list('da_party', flat=True).distinct().order_by('da_party')
        context['years'] = range(1900, 2024)
        context['selected_party'] = self.request.GET.get('party', '')
        context['selected_min_dob'] = self.request.GET.get('min_dob', '')
        context['selected_max_dob'] = self.request.GET.get('max_dob', '')
        context['selected_voter_score'] = self.request.GET.get('voter_score', '')
        context['selected_v20state'] = self.request.GET.get('v20state', '')
        context['selected_v21town'] = self.request.GET.get('v21town', '')
        context['selected_v21primary'] = self.request.GET.get('v21primary', '')
        context['selected_v22general'] = self.request.GET.get('v22general', '')
        context['selected_v23town'] = self.request.GET.get('v23town', '')

        # dob histogram
        birth_years = [v.da_dob.year for v in voters]
        fig = go.Bar(x=sorted(set(birth_years)), y=[birth_years.count(y) for y in sorted(set(birth_years))])
        title_text = f'Voter Distribution by Year of Birth'
        graph_div_dob = plotly.offline.plot({"data": [fig], "layout_title_text": title_text},
                                             auto_open=False, output_type="div")
        context['graph_div_dob'] = graph_div_dob

        # pie chart of partys
        parties = [v.da_party.strip() for v in voters]
        party_labels = sorted(set(parties))
        party_counts = [parties.count(p) for p in party_labels]
        fig = go.Pie(labels=party_labels, values=party_counts)
        title_text = f'Voter Distribution by Party Affiliation'
        graph_div_party = plotly.offline.plot({"data": [fig], "layout_title_text": title_text},
                                               auto_open=False, output_type="div")
        context['graph_div_party'] = graph_div_party
        # election particip histogram
        x = ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town']
        y = [
            voters.filter(da_v20state=True).count(),
            voters.filter(da_v21town=True).count(),
            voters.filter(da_v21primary=True).count(),
            voters.filter(da_v22general=True).count(),
            voters.filter(da_v23town=True).count(),
        ]
        fig = go.Bar(x=x, y=y)
        title_text = f'Voter Participation by Election'
        graph_div_elections = plotly.offline.plot({"data": [fig], "layout_title_text": title_text},
                                                   auto_open=False, output_type="div")
        context['graph_div_elections'] = graph_div_elections
        return context