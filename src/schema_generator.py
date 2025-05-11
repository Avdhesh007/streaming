import os
import json
import random
from typing import Dict, Any

class AvroSchemaConverter:
    @staticmethod
    def convert_avsc_to_class(avsc_path) -> Dict[str, Any]:
        """
        Read Avro schema file and return its contents
        
        :param avsc_path: Path to the .avsc file
        :return: Parsed Avro schema
        """
        # Read the Avro schema file
        with open(avsc_path, 'r') as f:
            schema = json.load(f)
        
        return schema
    
    @staticmethod
    def generate_random_data(avsc_path):
        """
        Generate random data based on the Avro schema
        
        :param avsc_path: Path to the .avsc file
        :return: Randomly generated data dictionary
        """
        # Read the Avro schema
        schema = AvroSchemaConverter.convert_avsc_to_class(avsc_path)
        
        # Create a random data generator based on schema
        def generate_random_value(field_type):
            if isinstance(field_type, list):
                # Handle union types, prioritize non-null type
                field_type = [t for t in field_type if t != 'null'][0]
            
            if field_type == 'int':
                return random.randint(1, 100)
            elif field_type == 'string':
                return f'test_{random.randint(1, 1000)}'
            elif field_type == 'boolean':
                return random.choice([True, False])
            else:
                return None
        
        # Generate random data for each field
        random_data = {}
        for field in schema.get('fields', []):
            random_data[field['name']] = generate_random_value(field['type'])
        
        return random_data
    
    @staticmethod
    def save_generated_class(avsc_path, output_path):
        """
        Save the Avro schema to a Python file
        
        :param avsc_path: Path to the .avsc file
        :param output_path: Path to save the generated Python class
        """
        # Read the Avro schema
        schema = AvroSchemaConverter.convert_avsc_to_class(avsc_path)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Generate a Python class representation
        class_content = f'# Generated Avro Schema Class\n\nclass {schema["name"]}:\n    def __init__(self, **kwargs):\n        """Initialize {schema["name"]} instance"""\n        for field in {schema["fields"]}:\n            setattr(self, field["name"], kwargs.get(field["name"]))\n'
        
        # Write the generated class to file
        with open(output_path, 'w') as f:
            f.write(class_content)
    
    @staticmethod
    def generate_random_data(avsc_path):
        """
        Generate random data based on the Avro schema
        
        :param avsc_path: Path to the .avsc file
        :return: Randomly generated instance of the Avro model
        """
        # Dynamically load the Avro model
        with open(avsc_path, 'r') as f:
            schema = f.read()
        
        # Create a dynamic Avro model
        DynamicModel = AvroModel.parse(schema)
        
        # Generate and return a random instance
        return DynamicModel.random()

# Example usage
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    avsc_path = os.path.join(current_dir, 'user_schema.avsc')
    output_path = os.path.join(current_dir, 'generated_user_model.py')
    
    # Convert schema to class and save
    AvroSchemaConverter.save_generated_class(avsc_path, output_path)
    
    # Generate random data
    random_user = AvroSchemaConverter.generate_random_data(avsc_path)
    print("Generated Random User:", random_user)
