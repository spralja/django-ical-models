from django.db import models


value_data_type_to_model = {
    'BINARY': NotImplementedError,
    'BOOLEAN': models.BooleanField,
    'CAL-ADDRESS': NotImplementedError,
    'DATE': models.DateField,
    'DATE-TIME': models.DateTimeField,
    'DURATION': NotImplementedError,
    'FLOAT': models.FloatField,
    'INTEGER': models.IntegerField,
    'PERIOD': NotImplementedError,
    'RECUR': NotImplementedError,
    'TEXT': models.TextField,
    'TIME': models.TimeField,
    'URI': NotImplementedError,
    'UTC-OFFSET': NotImplementedError, 
}


def create_property_field(value_data_type, conformance, **options):
    if not isinstance(value_data_type, str):
        raise TypeError(f'value_data_type must be str, not {type(value_data_type).__qualname__}')

    if value_data_type not in value_data_type_to_model:
        raise TypeError(f'value_data_type \'{value_data_type}\' not supported')
    
    field = value_data_type_to_model[value_data_type]

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
    