from django.contrib import auth
from django.contrib.auth.decorators import login_required
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework import status, generics
from django.contrib.auth.hashers import check_password
from ..models import User
from .. import serializers
from classes.models import Class, Class_user
from classes import serializers

"""
# 이메일 확인 완료
def send_email(request):
    subject = "message"
    to = ["seggle.sejong@gmail.com"]
    from_email = "seggle.sejong@gmail.com"
    message = "메지시 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()
"""

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully registered a new user"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
        return Response(data)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# class LogoutAllView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         tokens = OutstandingToken.objects.filter(user_id=request.user.username)
#         for token in tokens:
#             t, _ = BlacklistedToken.objects.get_or_create(token=token)
#         return Response(status=status.HTTP_205_RESET_CONTENT)

class UserInfoView(APIView):
    def get_object(self, username): # 존재하는 인스턴스인지 판단
        user = get_object_or_404(User, username = username)
        return user

    # 01-07 유저 조회
    # @login_required
    def get(self, request, username, format=None):
        user = self.get_object(username)
        try:
            serializer = serializers.UserInfoSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            raise Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    # 01-06 비밀번호 변경
    def patch(self, request, username):
        data = request.data
        current_password = data["current_password"]
        user = self.get_object(username)
        if check_password(current_password, user.password):
            new_password = data["new_password"]
            password_confirm = data["new_password2"]
            if new_password == password_confirm:
                user.set_password(new_password)
                user.save()
                return Response({'success': "비밀번호 변경 완료"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "새로운 비밀번호 일치하지 않음"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':"현재 비밀번호 일치하지 않음"}, status=status.HTTP_400_BAD_REQUEST)

    # 01-08 회원탈퇴
    def delete(self, request, username):
        data = request.data
        user = self.get_object(username)
        if check_password(data["password"], user.password):
            user.is_active = False
            user.save()
            return Response({'success': '회원 탈퇴 성공'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':"현재 비밀번호가 일치하지 않음"}, status=status.HTTP_400_BAD_REQUEST)


class ClassInfoView(APIView):
    # def get_object(self, username): # 존재하는 인스턴스인지 판단
    #     user = get_object_or_404(User, username = username)
    #     return user
    def get_object(self, class_id):
        classid = generics.get_object_or_404(Class, id = class_id)
        return classid

    # 01-09 유저 Class 조회
    def get(self, request):
        class_name_list = []
        class_lists = Class_user.objects.filter(username=request.user)
        for class_list in class_lists:
            #print(class_list)
            class_add_is_show = {}
            class_add = {}

            class_list_serializer = serializers.ClassGetSerializer(class_list.class_id)
            class_add_is_show = class_list_serializer.data
            class_add_is_show["is_show"] = class_list.is_show
            class_add['id'] = class_add_is_show['id']
            class_add['name'] = class_add_is_show['name']
            class_add['semester'] = str(class_add_is_show['year']) + '-' + str(class_add_is_show['semester']) + '학기'
            class_add['is_show'] = class_add_is_show['is_show']
            class_name_list.append(class_add)
        return Response(class_name_list, status=status.HTTP_200_OK)
    
    def patch(self, request):
        #class_id = kwargs.get('class_id')
        datas = request.data
        for data in datas:
            classid = self.get_object(data['class_id'])
            class_user = Class_user.objects.filter(username=request.user).filter(class_id=data['class_id'])
            if class_user.count() == 0:
                continue
            user = class_user[0]
            user.is_show = not user.is_show
            user.save(force_update=True)
        return Response("Success", status=status.HTTP_200_OK)