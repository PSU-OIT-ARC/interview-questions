import random
import string
from django.db import models

class Tag(models.Model):
    # Based on FlatUI
    BLACK = '#000000'      # Basic shade
    WHITE = '#ecf0f1'      # Light grey
    BLUE = '#3498db'       # Contrast: White
    GREEN = '#2ecc71'      # Contrast: White
    TURQUOISE = '#1abc9c'  # Contrast: White
    YELLOW = '#f1c40f'     # Contrast: White
    RED = '#e74c3c'        # Contrast: White
    PURPLE = '#9b59b6'     # Contrast: White

    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
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
            (Tag.WHITE , Tag.TURQUOISE),
            (Tag.WHITE , Tag.YELLOW),
            (Tag.WHITE , Tag.RED),
            (Tag.WHITE , Tag.PURPLE),
        )

        return random.choice(COLOR_COMBINATIONS)
