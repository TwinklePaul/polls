from sqlite3 import DataError
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django import forms
from dal import autocomplete

from .models import Vote, Choice, Poll


class CustomChoiceField(forms.ModelChoiceField):

    def label_from_instance(self, obj):
        if obj.image_url:
            return mark_safe("<img src='%s'/>" % obj.image_url)
        elif obj.image_file:
            # print("\n\n\n", obj.image_file.url)
            return mark_safe("<img src='%s'/>" % obj.image_file.url)
        else:
            return (obj)


class PollDetailForm(forms.ModelForm):
    choices = CustomChoiceField(queryset=None,
                                widget=forms.RadioSelect,
                                label=''
                                )

    class Meta:
        model = Poll
        fields = ['choices', ]

    def __init__(self, pk, *args, **kwargs):
        self.pk = pk
        super(PollDetailForm, self).__init__(*args, **kwargs)
        self.poll = Poll.objects.filter(id=self.pk)[0]
        self.fields['choices'] = CustomChoiceField(
            queryset=Choice.objects.filter(poll=self.poll.id),
            widget=forms.RadioSelect,
            label=''
        )

    def save(self, commit=True, **kwargs):
        choice = kwargs["choice"]
        choice_obj = Choice.objects.filter(id=choice.id)
        choice_obj.update(count_vote=choice_obj[0].count_vote+1)
        if len(Vote.objects.filter(
            poll=Poll.objects.filter(id=kwargs['poll'])[0],
            voter=kwargs['user']
        )) == 0:
            new_vote = Vote(
                poll=Poll.objects.filter(id=kwargs['poll'])[0],
                choice=choice_obj[0],
                voter=kwargs['user'])
            new_vote.save()
            return new_vote
        raise DataError("You have already Voted")


class VotesForm(forms.ModelForm):
    voter = forms.ModelChoiceField(
        queryset=get_user_model().objects.all()
    )
    poll = forms.ModelChoiceField(
        queryset=Poll.objects.all()
    )
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.all(),
        widget=autocomplete.ModelSelect2(
            url='choice-autocomplete', forward=('poll',))
    )

    class Meta:
        model = Vote
        fields = ('__all__')
