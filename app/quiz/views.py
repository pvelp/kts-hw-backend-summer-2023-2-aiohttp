from aiohttp.web_exceptions import HTTPBadRequest, HTTPConflict
from aiohttp_apispec import docs, request_schema, response_schema

from app.quiz.schemes import (
    ThemeSchema,
    ThemeListSchema,
    QuestionSchema
)
from app.web.app import View
from app.web.utils import json_response
from app.web.mixins import AuthRequiredMixin


# TODO: добавить проверку авторизации для этого View
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
        pass


class QuestionListView(AuthRequiredMixin, View):
    async def get(self):
        raise NotImplementedError
