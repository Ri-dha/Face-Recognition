from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def save_photo_with_new_name(photo, id_number, name):
    # Create a new name for the photo
    new_name = f"{id_number}_{name}"

    # Save the photo with the new name
    new_photo = default_storage.save(new_name, ContentFile(photo.read()))

    # Return the new photo
    return new_photo
