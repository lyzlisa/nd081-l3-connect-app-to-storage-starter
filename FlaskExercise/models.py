from FlaskExercise import app, db
from flask import flash
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import uuid


blob_container = app.config['BLOB_CONTAINER']
storage_url = f"https://{app.config['BLOB_ACCOUNT']}.blob.core.windows.net/"
blob_service = BlobServiceClient(account_url=storage_url, credential=app.config['BLOB_STORAGE_KEY'])


class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    scientific_name = db.Column(db.String(75))
    description = db.Column(db.String(800))
    image_path = db.Column(db.String(100))

    def __repr__(self):
        return '<Animal {}>'.format(self.body)

    def save_changes(self, file):
        if file:
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1]
            random_filename = str(uuid.uuid1())
            filename = random_filename + '.' + file_extension
            try:
                # Create a blob client using the local file name as the name for the blob
                blob_client = blob_service.get_blob_client(container=blob_container, blob=filename)

                print("\nUploading to Azure Storage as blob:\n\t" + filename)

                # Upload the created file
                blob_client.upload_blob(file.stream)

                if self.image_path:
                    blob_client = blob_service.get_blob_client(container=blob_container, blob=self.image_path)
                    print(f"\nDeleting blob:\n\t{self.image_path}")
                    blob_client.delete_blob()

            except Exception as err:
                flash(err)
            self.image_path = filename
        db.session.commit()
