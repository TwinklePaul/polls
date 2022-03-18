from django.urls import path

from .views import PollsListView, ChoicesListView, ChoiceAutocomplete
urlpatterns = [
    path("", PollsListView.as_view(), name="polls_list"),
    path("<uuid:pk>/", ChoicesListView.as_view(), name="poll"),
    path("choice-autocomplete/", ChoiceAutocomplete.as_view(),
         name='choice-autocomplete',),
    # path('<int:poll_id>/vote/', poll_vote, name='vote'),
    # path('end/<int:poll_id>/', endpoll, name='end_poll'),
]
