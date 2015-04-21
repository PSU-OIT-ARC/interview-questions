import json
import datetime
from unittest.mock import patch
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from model_mommy.mommy import make, prepare
from iq.questions.models import Question
from iq.tags.models import Tag
from iq.utils.tests import IqCustomTest


class TagModelsTest(IqCustomTest):
    """
    Tests models in the Tag app
    """
    def setUp(self):
        super(TagModelsTest, self).setUp()

    def test_tag_model(self):
        t = Tag (
            name = "test_tag",
        )
        random_colors = t.get_random_tag_colors()
        t.color = random_colors[0]
        t.background_color = random_colors[1]
        t.save()
        self.assertEqual(t.name, t.__str__())


#class TagViewsTest(IqCustomTest):
#    """
#    Tests view calls for Tag app
#    """
#    def setUp(self):
#        super(TagModelsTest, self).setUp()
#
#    def test_valid_to_json(self):
#        """
#        Ensures the appropriate tag data is instantiated into a json object
#        """
