from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from img.models import *
from img.serializer import *
from django.conf import settings
from PIL import Image,ImageOps



class ImageViews(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            serializer = ImageSerializer(data = request.data)
            if serializer.is_valid():
                image_data = serializer.save()
                image_url = str(settings.MEDIA_ROOT)+"/" + str(image_data.img)
                image_name = image_url.split("/")[-1].split(".")[0]
    

                #  Thumbnail image create
                thm_url = image_url.replace(image_name,image_name+"_thum")
                image = Image.open(image_url)
                size = (200,300)
                image.thumbnail(size)
                image.save(thm_url)

                # Grayscale image create
                gray_url = image_url.replace(image_name,image_name+"_gray")
                image = Image.open(image_url)
                grayscal = ImageOps.grayscale(image)
                grayscal.save(gray_url)

                # Medium image create
                mid_url = gray_url = image_url.replace(image_name,image_name+"_mid")
                image = Image.open(image_url)
                size=(500,500)
                resize_img = image.resize(size, resample = Image.BILINEAR)
                resize_img.save(mid_url)

                # Large image create
                large_url = image_url.replace(image_name,image_name+"_large")
                image = Image.open(image_url)
                size=(1024,768)
                resize_img = image.resize(size)
                resize_img.save(large_url)


            

                return Response({
                    'msg':'Image upload successfull', 
                    'img1':thm_url,
                    'img2':gray_url,
                    'img3':mid_url,
                    'img4':large_url
                    }, status=HTTP_201_CREATED)
        except  Exception as w:
            return Response({"msz": str(w)}, status=HTTP_400_BAD_REQUEST)

