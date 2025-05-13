# Avro Schema to Python Class Generator

## Overview
This project provides a tool to:
- Convert Avro schema (.avsc) files to Python classes
- Generate random data based on Avro schemas

## Prerequisites
- Python 3.8+
- Docker (optional, for Kafka)
- [Task](https://taskfile.dev/#/installation) (task runner)

## Setup
1. Install Task:
   - Windows: `winget install -e --id Go.Task`
   - macOS: `brew install go-task`
   - Linux: `sh -c "$(curl --location https://taskfile.dev/install.sh)"`

2. Set up virtual environment and install dependencies:
```bash
task setup
```

## Usage
### Task Commands
- `task`: Show available tasks
- `task test`: Run all tests
- `task generate`: Generate random data
- `task kafka:start`: Start local Kafka server
- `task stream:kafka`: Stream generated data to Kafka
- `task read:kafka`: Read data from Kafka

### Python Usage
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
