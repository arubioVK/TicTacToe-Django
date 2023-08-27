import factory
import factory.fuzzy

from tictactoe_app.models import Match
from users_app.factories import UserFactory

class MatchFactory(factory.django.DjangoModelFactory):

    class Meta: 
        model = Match

    player1 = factory.SubFactory(UserFactory)
    player2 = factory.SubFactory(UserFactory)
    finish = factory.fuzzy.FuzzyChoice(choices=[True, False])
    winner = factory.SubFactory(UserFactory)
    turn = factory.Faker('pyint', min_value=1, max_value=10)
    row0column0 = factory.SubFactory(UserFactory)
    row0column1 = factory.SubFactory(UserFactory)
    row0column2 = factory.SubFactory(UserFactory)
    row1column0 = factory.SubFactory(UserFactory)
    row1column1 = factory.SubFactory(UserFactory)
    row1column2 = factory.SubFactory(UserFactory)
    row2column0 = factory.SubFactory(UserFactory)
    row2column1 = factory.SubFactory(UserFactory)
    row2column2 = factory.SubFactory(UserFactory)