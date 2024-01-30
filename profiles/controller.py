from ninja import Router, File, NinjaAPI
from ninja.files import UploadedFile
from http import HTTPStatus

from django.shortcuts import get_object_or_404
from .models import Profile
from .schema import ProfileIn, ProfileOut

profiles_controller = Router(tags=['profiles'])


# get profile id_number
@profiles_controller.get('/{id_number}', response=ProfileOut)
def get_profile(request, id_number: int):
    profile = get_object_or_404(Profile, id_number=id_number)
    return profile


# create profile with image file upload
@profiles_controller.post('/', response=ProfileOut)
def create_profile(request, profile_in: ProfileIn, photo: UploadedFile = File(...)):
    profile = Profile.objects.create(**profile_in.dict(), photo=photo)
    return profile
