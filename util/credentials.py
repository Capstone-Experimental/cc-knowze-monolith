from google.oauth2 import service_account

credentials_path = 'util/cred.json'
credentials = service_account.Credentials.from_service_account_file(credentials_path)
