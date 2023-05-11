from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    question = models.CharField(max_length=255)

    def __str__(self):
        return self.question
    
    def get_answer(self):
        answers = Answer.objects.filter(question = self)
        data = []
        for answer in answers:
            data.append({
                'answer': answer.answer,
                'is_correct': answer.is_correct
            })
        
        return data


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.answer