from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from agents.mixins import OrganizerAndLoginRequiredMixin
from . import models, forms


class SignupView(generic.CreateView):
    form_class = forms.CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('login')


class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'


def landing_page(request):
    return render(request, 'landing.html')


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = models.Lead.objects.filter(organization=user.userprofile, agent__isnull=False)
        else:
            # user is agent
            queryset = models.Lead.objects.filter(organization=user.agent.organization, agent__isnull=False)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = models.Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
            context.update({
                'unassigned_leads': queryset
            })
        return context


def lead_list(request):
    # return HttpResponse('Hello world!')
    # return render(request, 'leads/lead_list.html')
    leads = models.Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/lead_list.html', context=context)


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user

        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = models.Lead.objects.filter(organization=user.userprofile)
        else:
            # user is agent
            queryset = models.Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


def lead_detail(request, pk):
    lead = models.Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_detail.html', context=context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = forms.LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        send_mail(
            subject='A lead has been created',
            message='go to see the site of the new lead',
            from_email='test@test.com',
            recipient_list=['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = forms.LeadModelForm
    if request.method == 'POST':
        form = forms.LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'form': form
    }
    return render(request, 'leads/lead_create.html', context=context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = forms.LeadModelForm

    def get_queryset(self):
        user = self.request.user
        return models.Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse('leads:lead-list')


class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assign_agent.html'
    form_class = None


def lead_update(request, pk):
    lead = models.Lead.objects.get(id=pk)
    form = forms.LeadModelForm(instance=lead)
    if request.method == 'POST':
        form = forms.LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {
        'lead': lead,
        'form': form
    }
    return render(request, 'leads/lead_update.html', context=context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse('leads:lead-list')

    def get_queryset(self):
        user = self.request.user
        return models.Lead.objects.filter(organization=user.userprofile)


def lead_delete(request, pk):
    lead = models.Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

# def lead_create(request):
#     """
#     this is only for reference
#     """
#     form = forms.LeadForm
#     if request.method == 'POST':
#         form = forms.LeadForm(request.POST)
#     if form.is_valid():
#         first_name = form.cleaned_data['first_name']
#         last_name = form.cleaned_data['last_name']
#         age = form.cleaned_data['age']
#         agent = models.Agent.objects.first()
#         models.Lead.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             age=age,
#             agent=agent
#         )
#         return redirect('/leads')
#     context = {
#         'form': form
#     }
#     return render(request, 'leads/lead_create.html', context=context)
