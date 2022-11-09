from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views import generic
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
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
    queryset = models.Lead.objects.all()
    context_object_name = 'leads'


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
    model = models.Lead
    context_object_name = 'lead'


def lead_detail(request, pk):
    lead = models.Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_detail.html', context=context)


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class = forms.LeadModelForm

    def get_success_url(self):
        return reverse('leads:lead-list')

    def form_valid(self, form):
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


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.Lead
    fields = '__all__'
    template_name = 'leads/lead_update.html'

    def get_success_url(self):
        return reverse('leads:lead-list')


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


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = models.Lead
    template_name = 'leads/lead_delete.html'

    def get_success_url(self):
        return reverse('leads:lead-list')


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
