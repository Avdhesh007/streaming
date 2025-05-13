import os
import pytest
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from schema_generator import AvroSchemaConverter

# Kafka test configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TEST_TOPIC = 'avro_schema_test_topic'

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

def test_kafka_streaming():
    """
    Test Kafka streaming functionality
    """
    import socket
    import time
    
    def is_kafka_available(host, port, timeout=10):
        """
        Check if Kafka broker is available
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                socket.create_connection((host, port), timeout=1)
                return True
            except (socket.timeout, ConnectionRefusedError):
                time.sleep(1)
        return False
    
    # Check if Kafka is available
    if not is_kafka_available('localhost', 9092):
        pytest.skip("Kafka broker not available")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    avsc_path = os.path.join(current_dir, '..', 'src', 'user_schema.avsc')
    
    # Generate multiple random data records
    random_data = [
        AvroSchemaConverter.generate_random_data(avsc_path) for _ in range(5)
    ]
    
    # Stream data to Kafka with retry mechanism
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            AvroSchemaConverter.stream_to_kafka(random_data, KAFKA_TEST_TOPIC, KAFKA_BOOTSTRAP_SERVERS)
            break
        except Exception as e:
            if attempt == max_attempts - 1:
                pytest.fail(f"Failed to stream data to Kafka after {max_attempts} attempts: {e}")
            time.sleep(5)  # Wait before retrying
    
    # Read data from Kafka with retry mechanism
    for attempt in range(max_attempts):
        try:
            received_data = AvroSchemaConverter.read_from_kafka(
                KAFKA_TEST_TOPIC, 
                KAFKA_BOOTSTRAP_SERVERS, 
                max_records=5
            )
            break
        except Exception as e:
            if attempt == max_attempts - 1:
                pytest.fail(f"Failed to read data from Kafka after {max_attempts} attempts: {e}")
            time.sleep(5)  # Wait before retrying
    
    # Validate received data
    assert len(received_data) == 5
    
    # Validate each record has the expected keys
    for record in received_data:
        assert 'id' in record
        assert 'name' in record
        assert 'email' in record
        assert 'age' in record
        assert 'active' in record
