"""Common helper functions"""
import re
import random
import string as _string


def generate_random_string(length):
    """
    Generate a string of requested length containing random uppercase
    characters (A-Z) and numbers (0-9) between
    """
    return ''.join(
        random.SystemRandom().choice(
            _string.ascii_uppercase + _string.digits
        ) for _ in range(length)
    )


def to_camel_case(string):
    """Converts string to camelCase"""
    parts = iter(string.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


def to_snake_case(string):
    """Convert string to snake_case"""
    string = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', string)
    string = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', string)
    string = string.replace("-", "_")
    string = string.replace(" ", "")
    return string.lower()


def remove_empty_objects(data, schema):
    """Removes empty objects from the provided array"""
    data = schema.dump(data)
    return [x for x in data if x != {}]


def validate_sparse_fieldsets(
        fields_to_return,
        requested_relations,
        resource_relations):
    """Validates and returns new schema based on requested fields"""
    columns_schema = fields_to_return[:]
    for relation in requested_relations:
        relation_array = relation.split('{')
        relation_fields = relation_array[0].split('.')
        if set(relation_fields).issubset(resource_relations.keys()):
            model = resource_relations[relation_fields[-1]]
            for field in [to_snake_case(x) for x in relation_array[1].split(',')]:
                if hasattr(model, field):
                    columns_schema.append(
                        relation_array[0] + '.' + to_snake_case(field))
    return columns_schema


def build_pagination_meta(users, request):
    """Builds the pagination meta object"""
    meta = {
        'page': users.page,
        'per_page': users.per_page,
        'count': users.total,
    }
    if users.page > 1:
        meta['prev'] = request.path + '?page=' + \
            str(users.page-1) + '&per_page=' + str(users.per_page)
    if users.page < users.total:
        meta['next'] = request.path + '?page=' + \
            str(users.page+1) + '&per_page=' + str(users.per_page)

    return meta
