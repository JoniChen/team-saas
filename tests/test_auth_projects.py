from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def register_and_login(email: str, password: str = "password123"):
      register_response = client.post("/auth/register",
                  json={"email": email, "password": password})
      assert register_response.status_code == 200

      login_response = client.post("/auth/login", 
                                   json={"email": email, "password": password})
      assert login_response.status_code == 200
      
      token = login_response.json()["access_token"]
      return {"Authorization": f"Bearer {token}"}

def test_users_only_see_projects_from_their_organization():
      unique = uuid4().hex

      user_a_headers = register_and_login(f"user-a-{unique}@example.com")
      user_b_headers = register_and_login(f"user-b-{unique}@example.com")

      org_a_reponse = client.post("/organizations/",
                                  json={"name": f"Org A {unique}"},
                                  headers=user_a_headers)
      assert org_a_reponse.status_code == 200

      org_b_reponse = client.post("/organizations/",
                                  json={"name": f"Org B {unique}"},
                                  headers=user_b_headers)
      assert org_b_reponse.status_code == 200

      project_a_response = client.post("/projects/",
                                       json={"name": "Project A"},
                                       headers=user_a_headers)
      assert project_a_response.status_code == 200

      project_b_response = client.post("/projects/",
                                       json={"name": "Project B"},
                                       headers=user_b_headers)
      assert project_b_response.status_code == 200
    
      user_b_projects = client.get("/projects/",headers=user_b_headers)     
      assert user_b_projects.status_code == 200
      assert len(user_b_projects.json()) == 1
      assert user_b_projects.json()[0]["name"] == "Project B"

def test_register_login_create_org_and_project_flow():
      unique = uuid4().hex
      email = f"test{unique}@example.com"
      password = "password123"
      org_name = f"Acme-{unique}"

      register_response = client.post(
          "/auth/register",
          json={"email": email, "password": password},
      )
      assert register_response.status_code == 200

      login_response = client.post(
          "/auth/login",
          json={"email": email, "password": password},
      )
      assert login_response.status_code == 200

      token = login_response.json()["access_token"]
      headers = {"Authorization": f"Bearer {token}"}

      project_before_org_response = client.post(
          "/projects/",
          json={"name": "Should fail"},
          headers=headers,
      )
      assert project_before_org_response.status_code == 400

      org_response = client.post(
          "/organizations/",
          json={"name": org_name},
          headers=headers,
      )
      assert org_response.status_code == 200

      project_response = client.post(
          "/projects/",
          json={"name": "Internal Tools"},
          headers=headers,
      )
      assert project_response.status_code == 200
      assert project_response.json()["name"] == "Internal Tools"

      projects_response = client.get("/projects/", headers=headers)  

      assert projects_response.status_code == 200
      assert len(projects_response.json()) == 1
      assert projects_response.json()[0]["name"] == "Internal Tools"