from django.views import generic
from django.shortcuts import reverse
from django.core.mail import send_mail

from leads.models import Agent
from . import forms, mixins

import random


class AgentListView(mixins.OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    context_object_name = 'agents'

    def get_queryset(self):
        queryset = self.request.user.userprofile
        return Agent.objects.filter(organization=queryset)


class AgentCreateView(mixins.OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = forms.AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent-list')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f'{random.randint(1_000_000, 9_999_999)}')
        user.save()
        Agent.objects.create(
            user=user, organization=self.request.user.userprofile
        )
        send_mail(
            subject='you are invited to be an agent',
            message='you were added as an agent on DJ CRM. please login to start.',
            from_email='dj@crm.com', recipient_list=(self.request.user.email,)

        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(mixins.OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agent_detail.html'

    def get_queryset(self):
        queryset = self.request.user.userprofile
        return Agent.objects.filter(organization=queryset)


class AgentUpdateView(mixins.OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    fields = ('organization',)

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        queryset = self.request.user.userprofile
        return Agent.objects.filter(organization=queryset)


class AgentDeleteView(mixins.OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'

    def get_success_url(self):
        return reverse('agents:agent-list')

    def get_queryset(self):
        queryset = self.request.user.userprofile
        return Agent.objects.filter(organization=queryset)
