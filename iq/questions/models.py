from django.db import models

class Question(models.Model):
    """
    Question object with text, answer, author, and associated tags
    """
    question_id = models.AutoField(primary_key=True)
    body = models.TextField()
    answer = models.TextField()
    difficulty = models.IntegerField(default=None, null=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('tags.Tag')

    def __str__(self):
        return self.body

    class Meta:
        db_table = "question"


class CategoryQuestion(models.Model):
    """
    Category / Question Intermediate Class
    """
    category_question_id = models.AutoField(primary_key=True)
    question = models.ForeignKey('questions.Question')
    category = models.ForeignKey('categories.Category')
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.body

    class Meta:
        db_table = "category_question_id"
