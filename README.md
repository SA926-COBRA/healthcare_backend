# Prontivus Backend

Medical management system backend API built with FastAPI.

## Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements-deploy.txt

# Set environment variables
cp env.example .env
# Edit .env with your database URL

# Run the application
python main.py
```

### Production Deployment

#### Render.com
```bash
# Deploy using render.yaml
# Set environment variables in Render dashboard:
# - DATABASE_URL
# - SECRET_KEY
# - ALLOWED_ORIGINS
```

#### Docker
```bash
# Build image
docker build -t prontivus-backend .

# Run container
docker run -p 8000:8000 -e DATABASE_URL=your_db_url prontivus-backend
```

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALLOWED_ORIGINS`: CORS allowed origins (comma-separated)
- `USE_SQLITE`: Set to "false" for PostgreSQL mode
- `ENVIRONMENT`: "production" or "development"

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Database

The application uses PostgreSQL in production mode. Ensure your database is properly configured and accessible.
