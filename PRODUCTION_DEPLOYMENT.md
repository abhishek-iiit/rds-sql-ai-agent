# 🚀 Production Deployment Guide

Your RDS Natural Language Query application is now **production-ready**! This guide will help you deploy it to various platforms.

## ✅ Production Features Implemented

- **Security**: Proper authentication, CSRF protection, security headers
- **Database**: PostgreSQL support with connection pooling
- **Static Files**: WhiteNoise for static file serving
- **Logging**: Comprehensive logging configuration
- **Health Checks**: Built-in health monitoring
- **Docker**: Production-ready containerization
- **Environment**: Proper environment variable handling
- **Performance**: Gunicorn with multiple workers
- **Monitoring**: Nginx reverse proxy with rate limiting

## 🎯 Quick Deployment Options

### Option 1: Docker Compose (Recommended for VPS)

```bash
# 1. Clone your repository
git clone https://github.com/abhishek-iiit/rds-sql-ai-agent.git
cd rds-sql-ai-agent

# 2. Run the deployment script
./deploy.sh
```

**Access your app at:**
- Frontend: http://localhost/frontend.html
- API: http://localhost/api/
- Admin: http://localhost/admin/ (admin/admin123)

### Option 2: Railway (Easiest Cloud Deployment)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy:**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables:**
   ```bash
   railway variables set DEBUG=False
   railway variables set SECRET_KEY=your-secret-key
   railway variables set ALLOWED_HOSTS=your-app.railway.app
   ```

### Option 3: Heroku

1. **Install Heroku CLI and Login:**
   ```bash
   heroku login
   ```

2. **Create Heroku App:**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables:**
   ```bash
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=your-app.herokuapp.com
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   heroku run python manage.py migrate --settings=rds_nl_query.settings_production
   ```

### Option 4: DigitalOcean App Platform

1. **Create App Spec File** (`app.yaml`):
   ```yaml
   name: rds-nl-query
   services:
   - name: web
     source_dir: /
     github:
       repo: abhishek-iiit/rds-sql-ai-agent
       branch: main
     run_command: gunicorn rds_nl_query.wsgi:application --bind 0.0.0.0:$PORT --workers 3
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: DEBUG
       value: "False"
     - key: SECRET_KEY
       value: your-secret-key
     - key: ALLOWED_HOSTS
       value: your-app.ondigitalocean.app
   ```

2. **Deploy via CLI:**
   ```bash
   doctl apps create --spec app.yaml
   ```

## 🔧 Environment Variables

Create a `.env` file or set these environment variables:

```bash
# Required
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=your-domain.com,your-app.railway.app

# Database (for Docker/PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=rds_nl_query
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Security (for HTTPS)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

## 🔒 Security Checklist

- ✅ **Secret Key**: Use a strong, unique secret key
- ✅ **Debug Mode**: Set to `False` in production
- ✅ **Allowed Hosts**: Specify your domain(s)
- ✅ **HTTPS**: Enable SSL/TLS in production
- ✅ **Database**: Use PostgreSQL with SSL
- ✅ **API Keys**: Store OpenAI keys securely
- ✅ **Rate Limiting**: Configured via Nginx
- ✅ **Security Headers**: XSS, CSRF, HSTS protection

## 📊 Monitoring & Maintenance

### Health Checks
- **Application**: `/api/connections/`
- **Database**: Built-in connection testing
- **Logs**: Available via `docker-compose logs -f`

### Performance Monitoring
- **Response Times**: Tracked in logs
- **Database Queries**: Django debug toolbar (dev only)
- **OpenAI Usage**: Monitor API costs

### Backup Strategy
- **Database**: Automated PostgreSQL backups
- **Code**: Git repository backups
- **Environment**: Document all configurations

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check database status
   docker-compose logs db
   
   # Reset database
   docker-compose down -v
   docker-compose up -d
   ```

2. **Static Files Not Loading**
   ```bash
   # Recollect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

3. **Permission Errors**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   chmod +x deploy.sh
   ```

4. **Port Already in Use**
   ```bash
   # Kill existing processes
   sudo lsof -ti:8000 | xargs kill -9
   ```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx/HAProxy)
- Multiple application instances
- Shared database connections
- Redis for session storage

### Performance Optimization
- Database connection pooling
- Query result caching
- CDN for static files
- Database indexing

### Cost Optimization
- Cache frequent queries
- Optimize OpenAI prompts
- Use appropriate instance sizes
- Monitor resource usage

## 🎉 Success Metrics

Your production deployment should have:

- ✅ **Response Time**: < 2 seconds for queries
- ✅ **Uptime**: > 99% availability
- ✅ **Security**: Pass security scans
- ✅ **Performance**: Handle concurrent users
- ✅ **Monitoring**: Real-time health checks

## 📞 Support

If you encounter issues:

1. Check the logs: `docker-compose logs -f`
2. Verify environment variables
3. Test database connectivity
4. Check OpenAI API key validity
5. Review security configurations

## 🔄 Updates & Maintenance

### Regular Maintenance
- Update dependencies monthly
- Monitor security advisories
- Backup database weekly
- Review logs for errors

### Deployment Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

---

**🎊 Congratulations! Your RDS Natural Language Query application is now production-ready and can handle real-world traffic securely and efficiently!**
