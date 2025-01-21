from django.db import models
from users.models import User

# TODO:on_delete


class Game():
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField()
    player = models.ForeignKey(User, on_delete=models.SET_NULL)
    player2 = models.ForeignKey(User, on_delete=models.SET_NULL)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL)
