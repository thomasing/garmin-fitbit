import os
from google.cloud import secretmanager

def create_secret(project_id, secret_id):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    project_detail = f"projects/{project_id}"
    response = client.create_secret(
        request={
            "parent": project_detail,
            "secret_id": secret_id,
            "secret": {"replication": {"automatic": {}}},
        }
    )
    return response

def create_secret_version(project_id, secret_id, data):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    parent = client.secret_path(project_id, secret_id)
    response = client.add_secret_version(
        request={"parent": parent, "payload": {"data": data.encode("UTF-8")}}
    )
    return response

def get_secret(project_id, secret_id, version_id):
    from google.cloud import secretmanager
    client = secretmanager.SecretManagerServiceClient()
    secret_detail = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": secret_detail})
    return response.payload.data.decode("UTF-8")
