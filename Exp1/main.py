from auth import get_gdrive_service
from crypto_utils import encrypt_file, decrypt_file, generate_key
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

def upload_file(service, filepath, filename):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("Uploaded file ID:", file.get('id'))
    return file.get('id')

def download_file(service, file_id, output_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

if __name__ == "__main__":
    # Initialize the Google Drive service
    service = get_gdrive_service()
    
    # Generate an AES encryption key
    key = generate_key()
    print("Generated AES Key:", key)
    
    # Prepare a sample file
    with open("mysecret.txt", "w", encoding="utf-8") as f:
        f.write("This is a confidential test file.")
        
    # Full secure workflow: Encrypt -> Upload -> Download -> Decrypt
    encrypt_file("mysecret.txt", "mysecret.enc", key)
    print("File encrypted.")
    
    file_id = upload_file(service, "mysecret.enc", "mysecret.enc")
    
    download_file(service, file_id, "mysecret_downloaded.enc")
    
    decrypt_file("mysecret_downloaded.enc", "mysecret_decrypted.txt", key)
    print('Decryption complete. Check mysecret_decrypted.txt')