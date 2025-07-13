# Hawaiian LeniLani Chatbot Deployment Guide

## 🌺 Overview

This directory contains all the deployment configuration for the Hawaiian LeniLani AI Consulting Chatbot. The system is designed to run on Docker with a microservices architecture that respects Hawaiian culture and business practices.

## 🏗️ Architecture

The deployment consists of the following services:

- **PostgreSQL** - Main database for conversations, leads, and analytics
- **Redis** - Cache and session storage
- **Rasa** - NLU engine for intent recognition and entity extraction
- **Rasa Actions** - Custom actions for Hawaiian business logic
- **FastAPI Backend** - Main API server with Claude integration
- **React Frontend** - Hawaiian-themed chat widget
- **Nginx** - Reverse proxy and load balancer
- **Backup Service** - Automated backup to local storage and S3

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space
- Valid API keys for:
  - Anthropic Claude API
  - HubSpot CRM
  - Google Calendar
  - AWS S3 (for backups)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/lenilani/hawaiian-chatbot.git
   cd hawaiian-chatbot/deployment
   ```

2. **Configure environment**
   ```bash
   cp .env.production .env
   # Edit .env with your actual API keys and passwords
   vim .env
   ```

3. **Deploy the application**
   ```bash
   ./deploy.sh deploy
   ```

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env.production`:

- `POSTGRES_PASSWORD` - Database password (required)
- `REDIS_PASSWORD` - Redis password (required)
- `ANTHROPIC_API_KEY` - Claude API key (required)
- `HUBSPOT_API_KEY` - HubSpot integration key
- `GOOGLE_CALENDAR_CLIENT_ID` - Google Calendar OAuth
- `SECRET_KEY` - Application secret key (required)
- `JWT_SECRET_KEY` - JWT signing key (required)

### Domain Configuration

Update the following for your domain:

1. In `.env.production`:
   - `DOMAIN=hawaii.lenilani.com`
   - `ALLOWED_ORIGINS=https://hawaii.lenilani.com`

2. In `nginx.conf`:
   - `server_name hawaii.lenilani.com;`

3. SSL certificates:
   - Place certificates in `ssl/` directory
   - Update paths in `nginx.conf`

## 🛠️ Deployment Commands

### Full Deployment
```bash
./deploy.sh deploy
```

### Service Management
```bash
./deploy.sh start      # Start all services
./deploy.sh stop       # Stop all services
./deploy.sh restart    # Restart all services
./deploy.sh status     # Check service status
```

### Logs and Debugging
```bash
./deploy.sh logs              # View all logs
./deploy.sh logs backend      # View specific service logs
docker-compose logs -f rasa   # Follow Rasa logs
```

### Backup Operations
```bash
./deploy.sh backup                    # Manual backup
docker exec backup /scripts/backup-postgres.sh   # PostgreSQL backup only
docker exec backup /scripts/backup-redis.sh      # Redis backup only
```

## 📊 Monitoring

### Health Checks
- Main health endpoint: `https://hawaii.lenilani.com/health`
- API health: `https://hawaii.lenilani.com/api/health`
- Rasa status: `http://localhost:5005/status`

### Metrics
- Prometheus metrics: `http://localhost:9090/metrics`
- Nginx status: `http://localhost/nginx-status`

### Database Queries
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U lenilani -d hawaiian_lenilani

# View conversation stats
SELECT * FROM analytics.daily_conversations ORDER BY date DESC LIMIT 7;

# Check island metrics
SELECT * FROM analytics.island_metrics;
```

## 🔒 Security

### SSL/TLS
- Use Let's Encrypt for free SSL certificates
- Certificates auto-renew via Certbot
- HSTS enabled with 1-year max-age

### Rate Limiting
- API: 10 requests/second per IP
- Chat: 30 requests/second per IP
- Configurable in `nginx.conf`

### Backup Security
- Encrypted backups to S3
- 7-day retention by default
- Automated daily backups

## 🌴 Hawaiian Cultural Integration

The deployment respects Hawaiian values:

- **Timezone**: All services use Pacific/Honolulu (HST)
- **Greetings**: Time-aware Hawaiian greetings
- **Language**: Supports Pidgin and standard English
- **Islands**: Island-specific business logic

## 🚨 Troubleshooting

### Common Issues

1. **Database connection failed**
   ```bash
   # Check PostgreSQL logs
   docker-compose logs postgres
   # Verify credentials in .env
   ```

2. **Rasa model not loading**
   ```bash
   # Retrain model
   docker-compose exec rasa rasa train
   # Check model directory
   docker-compose exec rasa ls -la /app/models
   ```

3. **Frontend not accessible**
   ```bash
   # Check Nginx configuration
   docker-compose exec nginx nginx -t
   # Restart Nginx
   docker-compose restart nginx
   ```

### Recovery Procedures

1. **Restore from backup**
   ```bash
   # List available backups
   docker exec backup ls -la /backup/postgres/
   
   # Restore specific backup
   docker exec backup /scripts/restore-postgres.sh hawaiian_lenilani_backup_20240115_020000.sql.gz
   ```

2. **Reset services**
   ```bash
   # Complete reset
   docker-compose down -v
   ./deploy.sh deploy
   ```

## 📈 Scaling

### Horizontal Scaling
- Backend: Increase `MAX_WORKERS` in `.env`
- Rasa: Deploy multiple instances behind load balancer
- PostgreSQL: Set up read replicas

### Performance Tuning
- Adjust `WORKER_TIMEOUT` for long conversations
- Increase Redis memory limit for more cache
- Enable query optimization in PostgreSQL

## 🏥 Maintenance

### Daily Tasks
- Monitor health endpoints
- Check backup completion
- Review error logs

### Weekly Tasks
- Analyze conversation metrics
- Update Rasa training data
- Review security logs

### Monthly Tasks
- Update dependencies
- Audit API usage
- Performance analysis

## 📞 Support

For deployment support:
- Documentation: [https://docs.lenilani.com](https://docs.lenilani.com)
- Issues: [https://github.com/lenilani/hawaiian-chatbot/issues](https://github.com/lenilani/hawaiian-chatbot/issues)
- Email: support@lenilani.com

## 🌺 Mahalo!

Thank you for deploying the Hawaiian LeniLani Chatbot. May it bring the spirit of Aloha to AI-powered business consulting!

---

*E komo mai (Welcome) to the future of Hawaiian business technology!*