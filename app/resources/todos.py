from flask import Response, request
from flask_restful import Resource
from mongoengine import ValidationError, FieldDoesNotExist

from app.databases import Todo
from app.resources.errors import SchemaValidationError
import logging

logger = logging.getLogger('flask-backend')


class TodoApi(Resource):
    def get(self):
        query = Todo.objects()
        logger.debug(query)
        todo_list = Todo.objects().to_json()
        return Response(todo_list, mimetype='application/json', status=200)

    def post(self):
        try:
            body = request.get_json()
            todo = Todo(**body)
            todo.save()
            id = todo.id
            return {'id': str(id)}, 200
        except(FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
