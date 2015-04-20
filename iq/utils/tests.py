import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from iq.questions.models import Question, CategoryQuestion
from iq.categories.models import Category
from iq.tags.models import Tag


class IqCustomTest(TestCase):
    """
    - Instantiates common objects needed to
    mimic behavior of a User
    - Applications inherit this instead of TestCase
    to use project-specific objects
    """
    def setUp(self):
        super(IqCustomTest, self).setUp()

        u = User(username="user", email="user@pdx.edu")
        u.set_password('foo')
        u.save()
        self.user = u

        c = Category (
            name = "Foo",
            description = "Something something",
            created_on = timezone.now(),
            created_by = self.user
        )
        c.save()
        self.category = c
