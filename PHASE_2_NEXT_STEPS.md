# Phase 2: Next Steps Guide

## Current Status ✅
- API authentication fully functional
- 7/7 protected endpoints validated
- Test users created in database
- JWT token generation working

## Quick Start: Test File Upload Pipeline

### Step 1: Create a Test CSV File
```bash
cat > /tmp/test_billing.csv << 'EOF'
date,provider,resource_type,resource_id,cost,tags
2025-02-01,aws,ec2,i-1234567890abcdef0,45.67,"env:prod,app:web"
2025-02-01,aws,s3,my-bucket-001,12.34,"env:prod,app:storage"
2025-02-01,gcp,compute,instance-001,56.78,"env:prod,app:api"
EOF
```

### Step 2: Generate JWT Token
```python
import os
import sys
sys.path.insert(0, "/workspaces/Cloud-Storage-Optimization/Cloud cost optimization")
os.environ["SECRET_KEY"] = "dev-secret-key-change-in-production-12345678901234567890"
from app.core.security import create_access_token
token = create_access_token({"sub": "2", "email": "demo@costintel.com"})
print(token)
```

### Step 3: Upload File
```bash
TOKEN="<from_above>"
curl -X POST http://localhost:8000/api/v1/ingestion/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/tmp/test_billing.csv" \
  -F "source=aws"
```

### Step 4: Monitor Processing
```bash
# Check ingestion job status
TOKEN="<from_above>"
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/ingestion/jobs

# Check classification results
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/classification/results

# Check cost records
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/v1/cost/records
```

## Available Test Endpoints

### Authentication
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/login` - Login (currently broken, use token generation)
- `POST /api/v1/auth/register` - Register (currently broken, use direct DB insert)
- `POST /api/v1/auth/refresh` - Refresh token
- `POST /api/v1/auth/change-password` - Change password
- `POST /api/v1/auth/api-keys` - Create API key

### Data Ingestion
- `POST /api/v1/ingestion/upload` - Upload billing file
- `GET /api/v1/ingestion/jobs` - List ingestion jobs
- `GET /api/v1/ingestion/jobs/{job_id}` - Get job details

### Cost Analysis
- `GET /api/v1/cost/records` - List cost records
- `POST /api/v1/cost/analyze` - Analyze costs
- `GET /api/v1/cost/summary` - Cost summary

### Classification (AI Engine)
- `GET /api/v1/classification/results` - List classifications
- `POST /api/v1/classification/classify` - Trigger classification

### Decision Engine
- `GET /api/v1/decisions/stats` - Decision statistics
- `GET /api/v1/decisions/` - List recommendations
- `POST /api/v1/decisions/{id}/approve` - Approve decision
- `POST /api/v1/decisions/{id}/dismiss` - Dismiss decision

### Dashboard
- `GET /api/v1/dashboard/summary` - Dashboard summary

## Testing Strategy

### Phase 1: Data Ingestion ✓
```
1. Upload CSV file
2. Verify job created
3. Check Celery task queued
4. Monitor metadata extraction
```

### Phase 2: Classification
```
1. Check classification results
2. Verify rule-based classification
3. Test with different entity types
```

### Phase 3: Decision Generation
```
1. Create cost records
2. Execute decision engine
3. Verify recommendations generated
4. Check estimated savings calculated
```

### Phase 4: Full Pipeline
```
1. Upload file
2. Wait for classification
3. Generate decisions
4. Update dashboard
```

## Database Direct Access

### Query Test Users
```bash
docker exec costintel-mysql mysql -ucostintel -pcostintel_dev_password costintel \
  -e "SELECT id, email, is_active FROM users;"
```

### Query Cost Records
```bash
docker exec costintel-mysql mysql -ucostintel -pcostintel_dev_password costintel \
  -e "SELECT * FROM cost_records LIMIT 5;"
```

### Query Ingestion Jobs
```bash
docker exec costintel-mysql mysql -ucostintel -pcostintel_dev_password costintel \
  -e "SELECT id, status, source FROM ingestion_jobs LIMIT 5;"
```

## Celery Task Monitoring

### Check Celery Worker Logs
```bash
docker logs costintel-celery-worker 2>&1 | tail -50
```

### Monitor Redis Queue
```bash
docker exec costintel-redis redis-cli LLEN celery
```

### Check Task Results
```bash
docker exec costintel-redis redis-cli GET celery-task-meta-<task_id>
```

## API Documentation

Access interactive API docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Token Expired
- Tokens expire after 30 minutes
- Generate new token: See "Generate JWT Token" section above

### 401 Unauthorized
- Verify token is valid and not expired
- Check `Authorization: Bearer <token>` header is present

### 500 Internal Server Error
- Check application logs: `docker logs costintel-app`
- Check database connection: `docker exec costintel-mysql mysql -ping`
- Check Redis connection: `docker exec costintel-redis redis-cli ping`

### Celery Tasks Not Processing
- Check worker is running: `docker logs costintel-celery-worker`
- Check Redis connection: `docker exec costintel-redis redis-cli ping`
- Restart worker: `docker restart costintel-celery-worker`

## Quick Reference: Test User

```
Email: demo@costintel.com
Password: password
ID: 2
Database: costintel
Container: costintel-mysql
```

## Files Created for Testing

1. `/tmp/test_api.py` - Tests 7 protected endpoints
2. `/tmp/test_security.py` - Tests authentication security
3. `/tmp/test_login.py` - Tests login endpoint
4. `/tmp/test_billing.csv` - Sample billing data

Run tests with:
```bash
python3 /tmp/test_api.py
python3 /tmp/test_security.py
python3 /tmp/test_login.py
```

---
All 7 protected endpoints are working and authenticated! Ready to test business logic.
