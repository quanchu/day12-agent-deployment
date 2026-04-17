# Deployment Information

## Public URL
https://student-deployment-day12.railway.app (Example URL)

## Platform
Railway

## Test Commands

### Health Check
```bash
curl https://student-deployment-day12.railway.app/health
# Expected: {"status": "ok", "uptime_seconds": ...}
```

### API Test (with authentication)
```bash
curl -X POST https://student-deployment-day12.railway.app/ask \
  -H "X-API-Key: student-secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I scale my AI agent?"}'
```

## Environment Variables Set
- `PORT`: 8000
- `AGENT_API_KEY`: student-secret-key-123
- `ENVIRONMENT`: production
- `LOG_LEVEL`: info
- `REDIS_URL`: (Railway provided URL)

## Screenshots
- [Deployment Dashboard](screenshots/railway_dashboard.png)
- [Service Logs](screenshots/running_logs.png)
- [Successful API Call](screenshots/test_curl.png)
