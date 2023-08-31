from aiohttp.web_exceptions import HTTPBadRequest, HTTPConflict, HTTPNotFound
from aiohttp_apispec import docs, request_schema, response_schema

from app.quiz.schemes import (
    ThemeSchema,
    ThemeListSchema,
    QuestionSchema, ThemeIdSchema, ListQuestionSchema
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @docs(tags=['quiz'], summary='Add a new theme')
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            title = data['title']
        except KeyError:
            raise HTTPBadRequest

        if await self.request.app.store.quizzes.get_theme_by_title(title):
            raise HTTPConflict

        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin, View):
    @docs(tags=['quiz'], summary='Get theme list')
    @response_schema(ThemeListSchema, 200)
    async def get(self):
        themes = await self.request.app.store.quizzes.list_themes()
        raw_themes = [ThemeSchema().dump(theme) for theme in themes]
        return json_response(data={'themes': raw_themes})


class QuestionAddView(AuthRequiredMixin, View):
    @docs(tags=['quiz'], summary='Add a new question')
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema, 200)
    async def post(self):
        data = await self.request.json()
        try:
            title = data['title']
            theme_id = data['theme_id']
            answers = data['answers']
        except Exception:
            raise HTTPBadRequest
        correct_answers = 0

        for answer in answers:
            if answer['is_correct']:
                correct_answers += 1
            if correct_answers > 1:
                raise HTTPBadRequest

        if correct_answers == 0:
            raise HTTPBadRequest

        if len(answers) == 1:
            raise HTTPBadRequest

        if await self.request.app.store.quizzes.get_question_by_title(title):
            raise HTTPConflict

        if await self.request.app.store.quizzes.get_theme_by_id(theme_id) is None:
            raise HTTPNotFound

        question = await self.request.app.store.quizzes.create_question(title, theme_id, answers)
        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @docs(tags=['quiz'], summary='Get questions list by theme_id')
    @request_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema, 200)
    async def get(self):
        try:
            theme_id = self.request.query.get('theme_id')
        except KeyError:
            theme_id = None
        questions = await self.request.app.store.quizzes.list_questions(theme_id)
        raw_questions = [QuestionSchema().dump(question) for question in questions]
        return json_response(data={'questions': raw_questions})

