from elasticmodels import Index, StringField, IntegerField, NestedField

class QuestionIndex(Index):
    class Meta:
        fields = [
            'body',
            'answer',
            'difficulty',
            'created_on',
        ]
        doc_type = "question"
