# Hospital Bulk Processing System

This project implements a bulk processing service that integrates with an existing
Hospital Directory API to handle CSV-based hospital creation and batch activation.

## Architecture Overview

CSV Upload → Bulk API → Hospital Directory API  
- Validates CSV input
- Creates hospitals with a shared batch ID
- Activates batch only after successful creation

## Tech Stack
- Python 3.10
- Django & Django REST Framework
- Requests (external API calls)
- Docker & Docker Compose
- Pytest

## API Endpoints

### Validate CSV
POST /hospitals/bulk/validate  
- Multipart form-data
- Validates structure and size (max 20 rows)

### Bulk Create Hospitals
POST /hospitals/bulk  
- Upload CSV file
- Creates hospitals via Hospital Directory API
- Activates batch upon full success

## CSV Format
```csv
name,address,phone
General Hospital,123 Main St,555-1234
