"""Example API usage and integration tests."""

import pytest
from httpx import ASGITransport, AsyncClient
from uuid import uuid4

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test health check endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


@pytest.mark.asyncio
async def test_auth_flow():
    """Test authentication flow."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        email = f"test-{uuid4().hex[:8]}@example.com"

        # Register
        register_data = {
            "email": email,
            "password": "SecurePassword123!",
            "full_name": "Test User",
        }
        response = await client.post("/api/v1/auth/register", json=register_data)
        assert response.status_code == 201
        
        # Login
        login_data = {
            "email": email,
            "password": "SecurePassword123!",
        }
        response = await client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert "refresh_token" in token_data
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        response = await client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_ingestion_endpoints():
    """Test ingestion endpoints require authentication."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Without auth - should fail
        response = await client.get("/api/v1/ingestion/jobs")
        assert response.status_code == 401
        
        # Dashboard stats - should fail without auth
        response = await client.get("/api/v1/dashboard/summary")
        assert response.status_code == 401


# Example curl commands for documentation
"""
# 1. Health Check
curl http://localhost:8000/health

# 2. Register User
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "full_name": "Test User"
  }'

# 3. Login (get token)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePassword123!"}'

# 4. Upload File (requires token)
curl -X POST http://localhost:8000/api/v1/ingestion/upload \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -F "file=@billing_export.csv"

# 5. Get Dashboard Summary
curl http://localhost:8000/api/v1/dashboard/summary \
  -H "Authorization: Bearer <YOUR_TOKEN>"

# 6. Get Cost Summary
curl http://localhost:8000/api/v1/cost/summary?months=3 \
  -H "Authorization: Bearer <YOUR_TOKEN>"

# 7. List Classifications
curl http://localhost:8000/api/v1/classification/results \
  -H "Authorization: Bearer <YOUR_TOKEN>"

# 8. List Decisions
curl http://localhost:8000/api/v1/decisions/ \
  -H "Authorization: Bearer <YOUR_TOKEN>"

# 9. Create API Key
curl -X POST http://localhost:8000/api/v1/auth/api-keys \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Production Integration"}'

# 10. Use API Key (alternative to JWT)
curl http://localhost:8000/api/v1/dashboard/summary \
  -H "X-API-Key: cintel_<YOUR_API_KEY>"
"""
