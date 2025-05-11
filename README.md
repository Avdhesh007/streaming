# Avro Schema to Python Class Generator

## Overview
This project provides a tool to:
- Convert Avro schema (.avsc) files to Python classes
- Generate random data based on Avro schemas

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
```python
from src.schema_generator import AvroSchemaConverter

# Convert Avro schema to Python class
AvroSchemaConverter.save_generated_class('schema.avsc', 'output_model.py')

# Generate random data
random_data = AvroSchemaConverter.generate_random_data('schema.avsc')
```

## Running Tests
```bash
pytest tests/
```
