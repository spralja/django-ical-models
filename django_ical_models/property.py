from django.db import models


_value_data_type_to_field_switch = {
    'BINARY': None,
    'BOOLEAN': models.BooleanField,
    'CAL-ADDRESS': None,
    'DATE': models.DateField,
    'DATE-TIME': models.DateTimeField,
    'DURATION': None,
    'FLOAT': models.FloatField,
    'INTEGER': models.IntegerField,
    'PERIOD': None,
    'RECUR': None,
    'TEXT': models.TextField,
    'TIME': models.TimeField,
    'URI': None,
    'UTC-OFFSET': None, 
}


def translate(string):
    return string.upper()


def create_property_field(value_data_type, conformance, **options):
    if not isinstance(value_data_type, str):
        raise TypeError('value_data_type must be str, not %s' % type(value_data_type).__qualname__)

    if not isinstance(conformance, str):
        raise TypeError('conformance must be str, not %s' % type(conformance).__qualname__)
        
    _value_data_type = value_data_type
    value_data_type = value_data_type.upper()

    if value_data_type not in _value_data_type_to_field_switch:
        raise TypeError('value_data_type \'%s\' not supported' % _value_data_type)

    if _value_data_type_to_field_switch[value_data_type] is None:
        raise NotImplementedError('value_data_type \'%s\' not implemented', _value_data_type)

    field = _value_data_type_to_field_switch[value_data_type]

    _conformance = conformance
    conformance = conformance.upper()

    if conformance == 'MUST BE SPECIFIED':
        if 'null' in options:
            if options['null']:
                raise TypeError('null=True is not supported with conformance=\'MUST BE SPECIFIED\'')

    elif conformance == 'CAN BE SPECIFIED':
        if 'primary_key' in options:
            if options['primary_key']:
                raise TypeError('primary_key=True is not supported with conformance=\'CAN BE SPECIFIED\'')

        if 'null' in options:
            if not options['null']:
                raise TypeError('null=False is not supported with conformance=\'CAN BE SPECIFIED\'')

        options['null'] = True

    elif conformance == 'CAN BE SPECIFIED MULTIPLE TIMES':
        raise NotImplementedError('conformance=\'CAN BE SPECIFIED MULTIPLE TIMES\' is not implemented yet')
        
    else:
        raise TypeError('\'%s\' is not a conformance' % _conformance)

    return field(**options)
    