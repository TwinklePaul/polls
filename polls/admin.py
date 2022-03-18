# from django import forms
from django.contrib import admin

from .models import Poll, Choice, Vote

from .forms import VotesForm


# class PollsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'pub_date')


class VotesAdmin(admin.ModelAdmin):
    form = VotesForm


admin.site.register(Poll)
admin.site.register(Choice)
admin.site.register(Vote, VotesAdmin)
