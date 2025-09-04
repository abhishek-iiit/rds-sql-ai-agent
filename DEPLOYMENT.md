# Production Deployment Guide

## Quick Start (Development)

1. **Setup Environment**
```bash
./setup.sh
```

2. **Configure Environment**
```bash
# Edit .env file with your credentials
nano .env
```

3. **Start Development Server**
```bash
source venv/bin/activate
python manage.py runserver
```

4. **Test the API**
- Open `frontend.html` in your browser
- Or use `python test_api.py`

## Production Deployment Options

### Option 1: Docker Deployment

1. **Build and Run**
```bash
docker-compose up -d
```

2. **Create Superuser**
```bash
docker-compose exec web python manage.py createsuperuser
```

### Option 2: AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 20.04 LTS
   - t3.medium or larger
   - Security group: HTTP (80), HTTPS (443), SSH (22)

2. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql-client
```

3. **Deploy Application**
```bash
git clone <your-repo>
cd rds-nl-query
./setup.sh
```

4. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/your/static/files/;
    }
}
```

5. **Setup Systemd Service**
```ini
[Unit]
Description=RDS NL Query
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/rds-nl-query
Environment=PATH=/home/ubuntu/rds-nl-query/venv/bin
ExecStart=/home/ubuntu/rds-nl-query/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 rds_nl_query.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### Option 3: AWS ECS Deployment

1. **Build and Push Docker Image**
```bash
docker build -t rds-nl-query .
docker tag rds-nl-query:latest <account-id>.dkr.ecr.<region>.amazonaws.com/rds-nl-query:latest
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/rds-nl-query:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "rds-nl-query",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::<account>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "rds-nl-query",
      "image": "<account-id>.dkr.ecr.<region>.amazonaws.com/rds-nl-query:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DEBUG",
          "value": "False"
        }
      ],
      "secrets": [
        {
          "name": "SECRET_KEY",
          "valueFrom": "arn:aws:secretsmanager:<region>:<account>:secret:rds-nl-query-secrets"
        }
      ]
    }
  ]
}
```

## Security Considerations

### 1. Environment Variables
- Never commit `.env` files
- Use AWS Secrets Manager in production
- Rotate API keys regularly

### 2. Database Security
- Use IAM database authentication
- Enable SSL/TLS connections
- Restrict database access by IP

### 3. API Security
- Implement rate limiting
- Add authentication/authorization
- Validate all inputs
- Use HTTPS only

### 4. OpenAI API Key Management
- Store keys securely
- Implement key rotation
- Monitor usage and costs

## Monitoring and Logging

### 1. Application Monitoring
```python
# Add to settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/rds-nl-query.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 2. AWS CloudWatch Integration
- Set up log groups
- Create custom metrics
- Configure alarms

### 3. Performance Monitoring
- Track query execution times
- Monitor OpenAI API usage
- Database connection pooling

## Scaling Considerations

### 1. Horizontal Scaling
- Use load balancer
- Multiple application instances
- Shared database connections

### 2. Caching
- Redis for query results
- Database query caching
- OpenAI response caching

### 3. Database Optimization
- Connection pooling
- Read replicas
- Query optimization

## Backup and Recovery

### 1. Database Backups
- Automated RDS snapshots
- Cross-region replication
- Point-in-time recovery

### 2. Application Backups
- Code repository backups
- Configuration backups
- Log archival

## Cost Optimization

### 1. OpenAI API Costs
- Cache frequent queries
- Optimize prompts
- Set usage limits

### 2. AWS Costs
- Right-size instances
- Use spot instances for dev
- Monitor and optimize

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check security groups
   - Verify credentials
   - Test network connectivity

2. **OpenAI API Errors**
   - Validate API key
   - Check rate limits
   - Monitor quotas

3. **Performance Issues**
   - Enable query logging
   - Check database indexes
   - Monitor resource usage