from django.contrib.auth.models import User
from ninja import Router, File, NinjaAPI
from ninja.files import UploadedFile
from http import HTTPStatus
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from .models import Profile
from .schema import ProfileIn, ProfileOut

profiles_controller = Router(tags=['profiles'])


# get profile id_number
@profiles_controller.get('/{id_number}', response=ProfileOut)
def get_profile(request, id_number: int):
    profile = get_object_or_404(Profile, id_number=id_number)
    return profile


#  create profile and user with photo save in profile
@profiles_controller.post('/', response=ProfileOut)
def create_profile(request, profile_in: ProfileIn, photo: UploadedFile = File(...)):
    user = User.objects.create_user(username=profile_in.username, password=profile_in.profile_password)
    profile = get_object_or_404(Profile, user=user)
    profile.name = profile_in.name
    profile.id_number = profile_in.id_number
    profile.profile_password = profile_in.profile_password
    profile.profile_email = profile_in.profile_email
    profile.refresh_token = profile_in.refresh_token
    # i want to change the name of the photo to the id_number of the profile and name before save
    new_photo = save_photo_with_new_name(photo, profile.id_number)

    profile.photo = new_photo
    profile.save()
    return profile


def save_photo_with_new_name(photo, id_number):
    # Create a new name for the photo
    new_name = f"{id_number}_{photo.name}"

    # Save the photo with the new name
    new_photo = default_storage.save(new_name, ContentFile(photo.read()))

    # Return the new photo
    return new_photo
