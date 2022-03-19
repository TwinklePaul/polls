from django.views.generic import ListView
from django.views.generic.edit import ModelFormMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from dal import autocomplete

from .models import Poll, Choice, Vote
from .forms import PollDetailForm


class PollsListView(LoginRequiredMixin, ListView):
    model = Poll
    template_name = "polls/home.html"
    context_object_name = "polls"
    login_url = "account_login"

    def get_context_data(self, **kwargs):
        context = super(PollsListView, self).get_context_data(**kwargs)
        status = []
        for poll in context['polls']:
            votes = poll.titles.all()
            if votes:
                if len(votes.filter(voter=self.request.user)) > 0:
                    status.append(False)
                else:
                    status.append(True)
            else:
                status.append(True)
        context['polls'] = zip(context['polls'], status)
        return context


class ChoicesListView(LoginRequiredMixin, ListView, ModelFormMixin):
    model = Choice
    form_class = PollDetailForm
    template_name = "polls/detail.html"
    context_object_name = "poll"
    login_url = "account_login"

    def get_queryset(self, **kwargs):
        self.poll = get_object_or_404(Poll, id=self.kwargs['pk'])
        # print("\n\n\n", Choice.objects.filter(poll=self.poll))
        return {'poll': self.poll, 'choices': Choice.objects.filter(poll=self.poll)}

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Poll, id=self.kwargs['pk'])
        self.form = PollDetailForm(pk=self.kwargs['pk'])
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.object = self.form.save(
                choice=self.form.cleaned_data["choices"], review=self.form.cleaned_data["review"], poll=self.kwargs['pk'], user=self.request.user)
            messages.success(request, f'{self.object} noted')
            self.form = PollDetailForm(pk=self.kwargs['pk'])
            return redirect('/polls/')

        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ChoicesListView, self).get_context_data(
            *args, **kwargs)
        context['form'] = PollDetailForm(pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self):
        kwargs = super(ChoicesListView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs


class ChoiceAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Choice.objects.none()

        qs = Choice.objects.all()
        poll = self.forwarded.get('poll', None)

        if poll:
            qs = qs.filter(poll=poll)

        return qs
