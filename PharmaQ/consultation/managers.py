from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class QuestionManager(models.Manager):

    def get_answer_creator(self, question_id):
        question = self.get(pk=question_id)
        answer = question.answers.get()
        answer_creator = UserModel.objects.get(id=answer.creator_id_id)
        return answer_creator.username

    def get_answer(self, question_id):
        question = self.get(pk=question_id)
        return question.answers.get()

    def get_question_creator(self, question_id):
        question = self.get(pk=question_id)
        creator = UserModel.objects.get(id=question.creator_id_id)
        return creator.username

    def get_answer_content(self, question_id):
        question = self.get(pk=question_id)
        answer = question.answers.get()
        answer_content = answer.content
        return answer_content

    def has_answer(self , question_id):
        question = self.get(pk=question_id)
        return question.answers.exists()

    def filter_by_creator(self, creator_id):
        return self.filter(creator_id=creator_id)

    def filter_by_is_public(self):
        return self.filter(is_public=True)

    def filter_by_is_answered(self):
        return self.filter(answers__isnull=True)


class AnswerManager(models.Manager):

    def filter_by_creator(self, creator_id):
        return self.filter(creator_id=creator_id)
