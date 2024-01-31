from django.contrib.auth.models import User
from ninja import Router, File
from ninja.files import UploadedFile
from profiles.utlis.savePhoto import save_photo_with_new_name
from django.shortcuts import get_object_or_404
from .models import Profile
from .schema import ProfileIn, ProfileOut, UpdateRefreshToken, UpdatePassword

profiles_controller = Router(tags=['profiles'])


@profiles_controller.get('/refresh_token/{refresh_token}', response=ProfileOut)
def get_by_refresh_token(request, refresh_token: str):
    profile = get_object_or_404(Profile, refresh_token=refresh_token)
    return profile

# get profile id_number
@profiles_controller.get('/{id_number}', response=ProfileOut)
def get_profile(request, id_number: int):
    profile = get_object_or_404(Profile, id_number=id_number)
    return profile


#  create profile and user with photo save in profile
@profiles_controller.post('/', response=ProfileOut)
def create_profile(request, profile_in: ProfileIn
                   , photo: UploadedFile = File(...)
                   ):
    user = User.objects.create_user(username=profile_in.username, password=profile_in.profile_password)
    profile = get_object_or_404(Profile, user=user)
    profile.name = profile_in.name
    profile.id_number = profile_in.id_number
    profile.profile_password = profile_in.profile_password
    profile.profile_email = profile_in.profile_email
    profile.refresh_token = profile_in.refresh_token
    new_photo = save_photo_with_new_name(photo, profile.id_number)

    profile.photo = new_photo
    profile.save()
    return profile


@profiles_controller.get('/name/{id_number}', response=ProfileOut)
def get_by_name(request, id_number: int):
    profile = get_object_or_404(Profile, id_number=id_number)
    return profile


@profiles_controller.put('/{id_number}', response=ProfileOut)
def update_refresh_token(request, id_number: int, update_refresh_token: UpdateRefreshToken):
    profile = get_object_or_404(Profile, id_number=id_number)
    profile.refresh_token = update_refresh_token.refresh_token
    profile.save()
    return profile


@profiles_controller.put('/{id_number}', response=ProfileOut)
def update_password(request, id_number: int, update_password: UpdatePassword):
    profile = get_object_or_404(Profile, id_number=id_number)
    profile.profile_password = update_password.profile_password
    profile.save()
    return profile
