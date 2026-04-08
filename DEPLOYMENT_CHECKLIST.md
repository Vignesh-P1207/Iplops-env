# IPLOps-Env Deployment Checklist

## Pre-Deployment Verification

### ✅ Code Quality
- [x] All Python files have proper imports
- [x] Type hints used throughout
- [x] Pydantic models for data validation
- [x] Error handling implemented
- [x] No hardcoded credentials
- [x] Logging configured

### ✅ Testing
- [x] Test suite created (`test_agent.py`)
- [x] Example agents work (`inference.py`, `example_custom_agent.py`)
- [x] All 3 tasks tested
- [x] API endpoints validated
- [x] Error cases handled

### ✅ Documentation
- [x] README.md complete
- [x] USAGE.md comprehensive
- [x] API_DOCS.md detailed
- [x] ARCHITECTURE.md clear
- [x] Code comments added
- [x] Examples provided

### ✅ Configuration
- [x] requirements.txt complete
- [x] Dockerfile working
- [x] openenv.yaml valid
- [x] .gitignore configured
- [x] Environment variables handled

## Local Testing

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```
**Expected**: All packages install without errors

### Step 2: Start Server
```bash
python app/main.py
```
**Expected**: Server starts on http://localhost:8000

### Step 3: Health Check
```bash
curl http://localhost:8000/health
```
**Expected**: `{"status": "healthy", ...}`

### Step 4: Run Tests
```bash
python test_agent.py
```
**Expected**: All 3 tasks complete with scores

### Step 5: Run Inference
```bash
python inference.py 1
python inference.py 2
python inference.py 3
```
**Expected**: Each task returns a score

## Docker Testing

### Step 1: Build Image
```bash
docker build -t iplops-env .
```
**Expected**: Image builds successfully

### Step 2: Run Container
```bash
docker run -p 8000:8000 iplops-env
```
**Expected**: Container starts, server accessible

### Step 3: Test from Host
```bash
curl http://localhost:8000/health
```
**Expected**: Health check passes

### Step 4: Stop Container
```bash
docker stop <container_id>
```

## Production Deployment

### Option 1: Docker Hub

```bash
# Tag image
docker tag iplops-env:latest yourusername/iplops-env:1.0.0

# Push to Docker Hub
docker push yourusername/iplops-env:1.0.0

# Pull and run on production
docker pull yourusername/iplops-env:1.0.0
docker run -d -p 8000:8000 --name iplops yourusername/iplops-env:1.0.0
```

### Option 2: AWS ECS

```bash
# Build for AWS
docker build -t iplops-env .

# Tag for ECR
docker tag iplops-env:latest <aws-account-id>.dkr.ecr.<region>.amazonaws.com/iplops-env:latest

# Push to ECR
docker push <aws-account-id>.dkr.ecr.<region>.amazonaws.com/iplops-env:latest

# Deploy via ECS console or CLI
```

### Option 3: Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/<project-id>/iplops-env

# Deploy
gcloud run deploy iplops-env \
  --image gcr.io/<project-id>/iplops-env \
  --platform managed \
  --port 8000 \
  --allow-unauthenticated
```

### Option 4: Heroku

```bash
# Login
heroku login

# Create app
heroku create iplops-env

# Set stack to container
heroku stack:set container

# Deploy
git push heroku main
```

### Option 5: DigitalOcean App Platform

```bash
# Use web interface or doctl CLI
doctl apps create --spec app.yaml
```

## Post-Deployment Verification

### ✅ Smoke Tests

1. **Health Check**
```bash
curl https://your-domain.com/health
```
Expected: `{"status": "healthy"}`

2. **Environment Info**
```bash
curl https://your-domain.com/
```
Expected: JSON with tasks and endpoints

3. **Task 1 Flow**
```bash
# Reset
curl -X POST https://your-domain.com/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": 1}'

# Step
curl -X POST https://your-domain.com/step \
  -H "Content-Type: application/json" \
  -d '{"action": {"security_per_gate": 5, "total_security": 80, "medical_personnel": 35, "ticketing_staff": 20}}'
```
Expected: Reward between 0.0 and 1.0

### ✅ Load Testing

```bash
# Install Apache Bench
apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 https://your-domain.com/health

# Test reset endpoint
ab -n 100 -c 5 -p reset.json -T application/json https://your-domain.com/reset
```

Expected: 
- 99% requests < 200ms
- 0% errors

### ✅ Monitoring Setup

1. **Application Logs**
```bash
# Docker
docker logs -f <container_id>

# Kubernetes
kubectl logs -f deployment/iplops-env
```

2. **Metrics to Track**
- Request rate (requests/second)
- Response time (p50, p95, p99)
- Error rate (%)
- CPU usage (%)
- Memory usage (MB)

3. **Alerts to Configure**
- Response time > 500ms
- Error rate > 1%
- CPU usage > 80%
- Memory usage > 80%

## Security Checklist

### ✅ Before Production

- [ ] Remove debug mode
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Enable HTTPS
- [ ] Set up authentication (if needed)
- [ ] Configure firewall rules
- [ ] Enable logging
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Document incident response

### ✅ Environment Variables

```bash
# Production settings
export ENVIRONMENT=production
export LOG_LEVEL=info
export CORS_ORIGINS=https://your-frontend.com
export MAX_REQUESTS_PER_MINUTE=100
```

## Rollback Plan

### If Deployment Fails

1. **Docker**
```bash
# Stop new container
docker stop <new_container_id>

# Start old container
docker start <old_container_id>
```

2. **Cloud Platforms**
```bash
# AWS ECS
aws ecs update-service --service iplops-env --task-definition iplops-env:previous

# Google Cloud Run
gcloud run services update-traffic iplops-env --to-revisions=previous=100

# Heroku
heroku rollback
```

## Maintenance

### Regular Tasks

**Daily**
- [ ] Check error logs
- [ ] Monitor response times
- [ ] Verify health checks

**Weekly**
- [ ] Review performance metrics
- [ ] Check disk usage
- [ ] Update dependencies (if needed)

**Monthly**
- [ ] Security audit
- [ ] Performance optimization
- [ ] Backup verification

### Updating the Application

```bash
# 1. Pull latest code
git pull origin main

# 2. Run tests
python test_agent.py

# 3. Build new image
docker build -t iplops-env:1.1.0 .

# 4. Test locally
docker run -p 8000:8000 iplops-env:1.1.0

# 5. Deploy to production
docker tag iplops-env:1.1.0 iplops-env:latest
docker push iplops-env:latest

# 6. Restart production container
docker-compose up -d
```

## Troubleshooting

### Common Issues

**Issue**: Server won't start
```bash
# Check logs
docker logs <container_id>

# Common causes:
# - Port 8000 already in use
# - Missing dependencies
# - Python version mismatch
```

**Issue**: High response times
```bash
# Check resource usage
docker stats <container_id>

# Solutions:
# - Increase container resources
# - Add horizontal scaling
# - Optimize code
```

**Issue**: Memory leaks
```bash
# Monitor memory over time
watch -n 1 docker stats <container_id>

# Solutions:
# - Restart container periodically
# - Fix memory leaks in code
# - Increase memory limit
```

## Success Criteria

### ✅ Deployment is Successful When:

- [ ] Health check returns 200 OK
- [ ] All 3 tasks work correctly
- [ ] Response times < 200ms (p95)
- [ ] Error rate < 0.1%
- [ ] CPU usage < 50%
- [ ] Memory usage < 70%
- [ ] Logs show no errors
- [ ] Monitoring dashboards green
- [ ] Documentation accessible
- [ ] Example agents work

## Final Checklist

### Before Going Live

- [ ] All tests pass
- [ ] Docker image builds
- [ ] Documentation complete
- [ ] Monitoring configured
- [ ] Alerts set up
- [ ] Backup plan ready
- [ ] Rollback tested
- [ ] Team trained
- [ ] Runbook created
- [ ] Support contacts listed

### After Going Live

- [ ] Announce to users
- [ ] Monitor for 24 hours
- [ ] Collect feedback
- [ ] Document issues
- [ ] Plan improvements
- [ ] Schedule review

---

## Quick Reference

### Essential Commands

```bash
# Local development
python app/main.py

# Run tests
python test_agent.py

# Build Docker
docker build -t iplops-env .

# Run Docker
docker run -p 8000:8000 iplops-env

# Check health
curl http://localhost:8000/health

# View logs
docker logs -f <container_id>

# Stop container
docker stop <container_id>
```

### Support Contacts

- **Technical Issues**: Check documentation first
- **Bug Reports**: Create GitHub issue
- **Feature Requests**: Submit via GitHub
- **Security Issues**: Email security@example.com

---

**Deployment Status**: ✅ Ready for Production

Last Updated: 2026-04-06
Version: 1.0.0
