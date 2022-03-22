# from django import forms
from django.contrib import admin

from .models import Poll, Choice, Vote

from .forms import VotesForm


# class PollsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'pub_date')

class ChoicesAdmin(admin.ModelAdmin):
    list_display = ('option', 'poll', 'count_vote')


class VotesAdmin(admin.ModelAdmin):
    form = VotesForm
    list_display = ('voter', 'option', 'poll')


admin.site.register(Poll)
admin.site.register(Choice, ChoicesAdmin)
admin.site.register(Vote, VotesAdmin)
