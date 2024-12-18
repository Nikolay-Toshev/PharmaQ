from django import template

from PharmaQ.consultation.models import Question

register = template.Library()

@register.simple_tag
def get_answer_creator(question_id):
    answer_creator = Question.objects.get_answer_creator(question_id)
    return answer_creator

@register.simple_tag
def get_question_creator(question_id):
    question_creator = Question.objects.get_question_creator(question_id)
    return question_creator

@register.simple_tag
def get_answer_content(question_id):
    answer_content = Question.objects.get_answer_content(question_id)
    return answer_content


@register.simple_tag
def has_answer(question_id):
    return Question.objects.has_answer(question_id)