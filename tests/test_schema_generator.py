import os
import pytest
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from schema_generator import AvroSchemaConverter

def test_avsc_to_class_conversion():
    """
    Test converting Avro schema to Python class
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    avsc_path = os.path.join(current_dir, '..', 'src', 'user_schema.avsc')
    
    # Test conversion method
    schema = AvroSchemaConverter.convert_avsc_to_class(avsc_path)
    
    # Check if schema has expected attributes
    assert schema['name'] == 'User'
    assert schema['fields'][0]['name'] == 'id'
    assert schema['fields'][0]['type'] == 'int'

def test_random_data_generation():
    """
    Test generating random data from Avro schema
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    avsc_path = os.path.join(current_dir, '..', 'src', 'user_schema.avsc')
    
    # Generate random data
    random_user = AvroSchemaConverter.generate_random_data(avsc_path)
    
    # Validate generated data
    assert 'id' in random_user
    assert 'name' in random_user
    assert 'email' in random_user
    assert 'age' in random_user
    assert 'active' in random_user

def test_save_generated_class():
    """
    Test saving generated class to a file
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    avsc_path = os.path.join(current_dir, '..', 'src', 'user_schema.avsc')
    output_path = os.path.join(current_dir, '..', 'src', 'test_generated_model.py')
    
    # Save generated class
    AvroSchemaConverter.save_generated_class(avsc_path, output_path)
    
    # Check if file was created
    assert os.path.exists(output_path)
    
    # Clean up the generated file
    os.remove(output_path)
