from django.conf import settings
from arcutils import ChoiceEnum

class QuestionOrderChoices(ChoiceEnum):
    BODY = 1
    CREATED_ON = 2
    CREATED_BY = 4
    DIFFICULTY = 8

    _choices = (
            ('','Filter by:'),
            (BODY, "Question body"),
            (CREATED_ON, "Most recent"),
            (CREATED_BY, "Author"),
            (DIFFICULTY, "Difficulty"),
            )
