import httpx
import time

BASE_URL = "http://localhost:8001/api"


def verify_subjects_crud():
    print("Verifying Subjects CRUD...")

    # 1. Create a Subject with nested Chapters and Topics
    print("Creating Subject with NO nested items (Baseline)...")
    subject_data = {"class_name": "Class 11", "subject_name": "Physics Baseline"}
    response = httpx.post(f"{BASE_URL}/subjects/", json=subject_data)
    if response.status_code != 200:
        print(f"Failed to create subject: {response.text}")
        return
    subject = response.json()
    subject_id = subject["id"]
    print(f"Subject created: {subject}")

    # Clean up baseline
    httpx.delete(f"{BASE_URL}/subjects/{subject_id}")

    print("\nCreating Subject WITH Nested Chapters and Topics...")
    nested_subject_data = {
        "class_name": "Class 12",
        "subject_name": "Chemistry Nested",
        "chapters": [
            {
                "no": "1",
                "name": "Solid State",
                "topics": [
                    {"no": "1.1", "name": "Crystalline Solids"},
                    {"no": "1.2", "name": "Amorphous Solids"},
                ],
            },
            {"no": "2", "name": "Solutions", "topics": []},
        ],
    }

    response = httpx.post(f"{BASE_URL}/subjects/", json=nested_subject_data)
    if response.status_code != 200:
        print(f"Failed to create nested subject: {response.text}")
        return

    subject = response.json()
    subject_id = subject["id"]
    print(f"Nested Subject Created: {subject}")

    # Verify DB state by fetching
    print("Fetching to verify nesting...")
    response = httpx.get(f"{BASE_URL}/subjects/{subject_id}")
    full_subject = response.json()

    chapters = full_subject["chapters"]
    assert len(chapters) == 2

    # Sort chapters by 'no' to ensure deterministic checks
    chapters.sort(key=lambda x: x["no"])

    assert chapters[0]["name"] == "Solid State"
    assert len(chapters[0]["topics"]) == 2

    assert chapters[1]["name"] == "Solutions"
    assert len(chapters[1]["topics"]) == 0

    print("Nested creation verified successfully!")

    # Clean up
    print("Deleting Subject...")
    httpx.delete(f"{BASE_URL}/subjects/{subject_id}")
    print("Subject deleted.")


if __name__ == "__main__":
    try:
        verify_subjects_crud()
    except Exception as e:
        print(f"Verification failed with exception: {e}")
