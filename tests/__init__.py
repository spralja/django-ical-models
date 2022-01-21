import unittest
import django_ical_models

class PropertyFieldTestCase(unittest.TestCase):
    def test_value_data_type_not_str(self):
        value_data_type = 123
        conformance = 'CAN BE SPECIFIED'
        try:
            django_ical_models.create_property_field(value_data_type, conformance)
            with self.assertRaises(TypeError):
                django_ical_models.create_property_field(value_data_type, conformance)
        except TypeError as e:
            self.assertEqual(str(e), 'value_data_type must be str, not int')

    def test_conformance_not_str(self):
        value_data_type = 'TEXT'
        conformance = 123
        try:
            django_ical_models.create_property_field(value_data_type, conformance)
            with self.assertRaises(TypeError):
                django_ical_models.create_property_field(value_data_type, conformance)
        except TypeError as e:
            self.assertEqual(str(e), 'conformance must be str, not int')
    
    def test_unsuported_value_data_type(self):
        value_data_type = 'TEST'
        conformance = 'CAN BE SPECIFIED'
        try:
            django_ical_models.create_property_field(value_data_type, conformance)
            with self.assertRaises(TypeError):
                django_ical_models.create_property_field(value_data_type, conformance)
        except TypeError as e:
            self.assertEqual(str(e), 'value_data_type \'TEST\' not supported')

    def test_unsuported_conformance(self):
        value_data_type = 'TEXT'
        conformance = 'TEST'
        try:
            django_ical_models.create_property_field(value_data_type, conformance)
            with self.assertRaises(TypeError):
                django_ical_models.create_property_field(value_data_type, conformance)
        except TypeError as e:
            self.assertEqual(str(e), '\'TEST\' is not a conformance')
    
    def test_MUST_BE_SPECIFIED_and_null_True(self):
        value_data_type = 'TEXT'
        conformance = 'MUST BE SPECIFIED'
        with self.assertRaises(TypeError):
            django_ical_models.create_property_field(value_data_type, conformance, null=True)
    
    def test_CAN_BE_SPECIFIED_and_primary_key_True(self):
        value_data_type = 'TEXT'
        conformance = 'CAN BE SPECIFIED'
        with self.assertRaises(TypeError):
            django_ical_models.create_property_field(value_data_type, conformance, primary_key=True)

    def test_CAN_BE_SPECIFIED_and_null_False(self):
        value_data_type = 'TEXT'
        conformance = 'CAN BE SPECIFIED'
        with self.assertRaises(TypeError):
            django_ical_models.create_property_field(value_data_type, conformance, null=False)
            