import os
import sys
import uuid

from fastapi.testclient import TestClient

# Ensure the app module in /src is importable
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT, "src")
sys.path.insert(0, SRC_DIR)

import app as app_module  # noqa: E402

client = TestClient(app_module.app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Sanity check for a known activity
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = f"test+{uuid.uuid4().hex}@example.com"

    # Ensure email not already present
    assert email not in app_module.activities[activity]["participants"]

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Verify via GET
    get_resp = client.get("/activities")
    assert get_resp.status_code == 200
    participants = get_resp.json()[activity]["participants"]
    assert email in participants

    # Unregister
    del_resp = client.delete(f"/activities/{activity}/participants?email={email}")
    assert del_resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
