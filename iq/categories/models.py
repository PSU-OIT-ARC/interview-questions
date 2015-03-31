from django.db import models

class Category(models.Model):
    """
    Named category containing a list of associated questions
    """

    # Colors are based off of bootstrap's message tag colors
    BLACK = '#000000'      # Basic
    WHITE = '#ffffff'      # Basic
    BLUE = '#337ab7'       # Contrast: White
    GREEN = '#5cb85c'      # Contrast: White
    TURQUOISE = '#5bc0de'  # Contrast: White
    YELLOW = '#f0ad4e'     # Contrast: White
    RED = '#d9534f'        # Contrast: White
    PURPLE = '#6f5499'     # Contrast: White

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    color = models.CharField(max_length=16)
    background_color = models.CharField(max_length=16)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"

    # I think we can scrap this
    @staticmethod
    def get_random_cat_colors():
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
