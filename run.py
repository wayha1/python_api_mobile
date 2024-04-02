from app import create_app, db
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = create_app()

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'skin-me-aa7d4f34b5d0.json'
PARENT_FOLDER_ID = "1WwCeyIf5Hnm5NZdxchTuId7G482_rOCg"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds
    
def upload_photo(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    
    file_metadata = {
        'name':"Hello",
        'parents': [PARENT_FOLDER_ID]
    }
    
    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()
    
upload_photo("Project skinme (1).pdf")

with app.app_context():
    from app.models import *
    db.create_all()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
