import secrets
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile


class Poll(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="user",
    )
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('poll', kwargs={'pk': str(self.pk)})

    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()

    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.option
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res


class Choice(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="choices")
    option = models.CharField(max_length=200)
    image_file = models.ImageField(
        upload_to='static/images', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    count_vote = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.option}"

    def save(self, *args, **kwargs):
        if self.image_url and not self.image_file:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(self.image_url).read())
            img_temp.flush()
            self.image_file.save(f"image_{self.pk}", File(img_temp))
        super(Choice, self).save(*args, **kwargs)

    @property
    def get_vote_count(self):
        return self.vote_set.count()


class Vote(models.Model):
    voter = models.ForeignKey(
        get_user_model(),
        on_delete=models.DO_NOTHING,
        related_name="voter",
    )

    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name="titles")

    choice = models.ForeignKey(
        Choice,
        related_name="chosen_vote",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.voter}'s vote on '{self.poll}'"

    def save(self, *args, **kwargs):
        if self.choice.poll.id != self.poll.id:
            raise ValueError("Please Select the Correct Value")
        super().save(*args, **kwargs)
