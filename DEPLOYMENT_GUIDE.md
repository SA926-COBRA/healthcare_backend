# Prontivus Deployment Guide

## 🚀 Deployment Options

### Option 1: Render.com (Recommended)

#### Prerequisites
- GitHub repository with your Prontivus code
- Render.com account (free tier available)

#### Steps

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `backend` folder as the root directory

3. **Configure the service**
   - **Build Command**: `pip install -r requirements-deploy.txt`
   - **Start Command**: `python deploy_main.py`
   - **Environment**: `Python 3`

4. **Set Environment Variables**
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   SECRET_KEY=your-super-secret-key
   ENVIRONMENT=production
   DEBUG=false
   USE_SQLITE=false
   USE_DATABASE=true
   ALLOWED_ORIGINS=https://your-frontend-url.com
   PORT=8000
   HOST=0.0.0.0
   ```

5. **Create PostgreSQL Database**
   - In Render dashboard, create a new PostgreSQL database
   - Copy the connection string to `DATABASE_URL`

### Option 2: Docker Deployment

#### Build and Run Locally
```bash
# Build the image
docker build -t prontivus-backend .

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@host:port/database \
  -e SECRET_KEY=your-secret-key \
  prontivus-backend
```

#### Deploy to Docker Hub
```bash
# Tag the image
docker tag prontivus-backend your-username/prontivus-backend

# Push to Docker Hub
docker push your-username/prontivus-backend
```

### Option 3: Traditional VPS Deployment

#### Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-pip -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Nginx (for reverse proxy)
sudo apt install nginx -y
```

#### Application Setup
```bash
# Clone repository
git clone https://github.com/your-username/prontivus.git
cd prontivus/backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements-deploy.txt

# Set up environment variables
cp env.example .env
# Edit .env with your production values

# Run database migrations
python -c "from app.database.database import init_db; init_db()"

# Start the application
python deploy_main.py
```

## 🔧 Environment Variables

### Required Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key (generate a strong one)
- `ENVIRONMENT`: Set to `production`
- `DEBUG`: Set to `false`

### Optional Variables
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `REDIS_URL`: Redis connection for background tasks
- `SMTP_*`: Email configuration for notifications

## 📊 Database Setup

### PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE prontivus_db;

-- Create user
CREATE USER prontivus_user WITH PASSWORD 'secure_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE prontivus_db TO prontivus_user;
ALTER USER prontivus_user CREATEDB;
```

### Data Migration
The application will automatically create tables on startup. Your synchronized data from SQLite is already in PostgreSQL.

## 🔒 Security Considerations

1. **Use strong SECRET_KEY**
2. **Enable HTTPS** (use Let's Encrypt for free SSL)
3. **Set up firewall** rules
4. **Regular backups** of PostgreSQL database
5. **Monitor logs** for security issues

## 📈 Monitoring

### Health Checks
- Endpoint: `GET /health`
- Returns: `{"status": "healthy", "database": "connected"}`

### Logs
- Application logs are written to stdout
- Use `structlog` for structured logging
- Consider Sentry for error tracking

## 🚀 Performance Optimization

1. **Database Connection Pooling**: Already configured
2. **Caching**: Use Redis for session storage
3. **CDN**: Serve static files through CDN
4. **Load Balancing**: Use multiple instances behind a load balancer

## 📞 Support

For deployment issues:
1. Check the logs in your deployment platform
2. Verify environment variables are set correctly
3. Ensure database connectivity
4. Check firewall and network settings

## 🎯 Next Steps

After successful deployment:
1. Test all API endpoints
2. Set up monitoring and alerts
3. Configure automated backups
4. Set up CI/CD pipeline
5. Deploy frontend application
