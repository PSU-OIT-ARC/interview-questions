import random
import string
from django.db import models

class Tag(models.Model):
    BLACK = '#000000'
    WHITE = '#ecf0f1'

    BLUE = '#428bca'
    GREEN = '#5cb85c'
    YELLOW = '#f0ad4e'
    RED = '#d9534f'
    CYAN = '#5bc0de'

    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    color = models.CharField(max_length=16)
    background_color = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    class Meta:
       db_table = "tag"

    # All glory for this goes to kfarr and mlp
    @staticmethod
    def get_random_tag_colors():
        """
        Returns a random set of tag color combinations
        """
        COLOR_COMBINATIONS = (
            (Tag.WHITE , Tag.BLUE),
            (Tag.WHITE , Tag.GREEN),
            (Tag.WHITE , Tag.YELLOW),
            (Tag.WHITE , Tag.RED),
            (Tag.WHITE , Tag.CYAN),
        )
        return random.choice(COLOR_COMBINATIONS)
