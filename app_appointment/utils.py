import json


def get_boolean_value(value):
    return json.loads(value.lower())


def save_validated_data(data_list, kwarg_list):
    """
    Return dictionary of validated data in base serializer save method
    """
    return dict(list(data_list) + list(kwarg_list))
