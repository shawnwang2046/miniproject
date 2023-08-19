import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.mark.parametrize(
    "topic_ids,expected_names",
    [([0, 1], ["Understanding Debt Consolidation: Laws, Regulations, and Costs", "Creating an Inclusive Workforce: Cultivating Diversity, Empowering Employees, and Fostering a C..."])],
)
def test_get_topic_names(topic_ids, expected_names):
    response = client.get(f"/get_topic_names/?topic_ids={','.join(map(str, topic_ids))}")
    assert response.status_code == 200
    assert response.json() == expected_names


@pytest.mark.asyncio
async def test_extract_topic_from_url():
    base_url = "http://localhost:8000"
    url_to_extract = "https://www.example.com"  # Replace with your actual URL
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/extract_topic", json={"url": url_to_extract})
    assert response.status_code == 200
    assert "url" in response.json()
    assert "topics" in response.json()