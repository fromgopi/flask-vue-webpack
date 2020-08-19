from .todos import TodoApi


def initialize_routes(api):
    api.add_resource(TodoApi, '/api/todos')
