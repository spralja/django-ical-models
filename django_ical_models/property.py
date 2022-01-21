from django.db import models


match_value_data_type_to_model = {
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


def match_value_data_type_to_model(value_data_type):
    match value_data_type:
        case 'BOOLEAN':
            return models.BooleanField
        case 'DATE':
            return models.DateField
        case 'DATE-TIME':
            return models.DateTimeField
        case 'FLOAT':
            return models.FloatField
        case 'INTEGER':
            return models.IntegerField
        case 'TEXT':
            return models.TextField
        case 'TIME':
            return models.TimeField
        case 'BINARY' | 'CAL-ADDRESS' | 'DURATION' | 'PERIOD' | 'RECUR' | 'URI' | 'UTC-OFFSET':
            raise NotImplementedError('value_data_type \'%s\' not implemented' % value_data_type)
        case _:
            raise TypeError('value_data_type \'%s\' not supported' % value_data_type)


def create_property_field(value_data_type, conformance, **options):
    if not isinstance(value_data_type, str):
        raise TypeError(f'value_data_type must be str, not {type(value_data_type).__qualname__}')

    field = match_value_data_type_to_model(value_data_type)

    if not isinstance(conformance, str):
        raise TypeError(f'conformance must be str, not {type(conformance).__qualname__}')

    match conformance:
        case 'MUST BE SPECIFIED':
            if 'null' in options:
                if options['null']:
                    raise TypeError(f'null must not be True with conformance \'{conformance}\'')

        case 'CAN BE SPECIFIED':
            if 'primary_key' in options:
                if options['primary_key']:
                    raise TypeError(f'primary_key must not be True with conformance \'{conformance}\'')
            
            if 'null' in options:
                if not options['null']:
                    raise TypeError(f'null must not be False with conformance \'{conformance}\'')

            else:
                options['null'] = True
        
        case 'CAN BE SPECIFIED MULTIPLE TIMES':
            raise NotImplementedError('conformance \'CAN BE SPECIFIED MULTIPLE TIMES\' is not implemented yet')
        
        case _:
            raise TypeError(f'\'{conformance}\' is not a conformance')

    return field(**options)
    