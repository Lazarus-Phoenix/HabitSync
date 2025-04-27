# import pytest
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
# User = get_user_model()
#
#
# @pytest.fixture
# def api_client():
#     return APIClient()
#
#
# @pytest.fixture
# def user():
#     return User.objects.create_user(
#         email="test@example.com", password="testpassword"
#     )
#
#
# @pytest.fixture
# def superuser():
#     return User.objects.create_superuser(
#         email="admin@example.com", password="adminpassword"
#     )
#
#
# @pytest.mark.django_db
# class TestUserViewSet:
#     def test_user_list(self, api_client, user, superuser):
#         api_client.force_authenticate(user=superuser)
#         url = reverse("users-list")
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) >= 1
#
#     def test_user_retrieve(self, api_client, user, superuser):
#         api_client.force_authenticate(user=superuser)
#         url = reverse("users-detail", kwargs={"pk": user.pk})
#         response = api_client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["email"] == user.email
#
#     def test_user_create(self, api_client):
#         url = reverse("register")
#         data = {
#             "email": "newuser@example.com",
#             "password": "newpassword",
#         }
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_201_CREATED
#         assert User.objects.filter(email="newuser@example.com").exists()
#         new_user = User.objects.get(email="newuser@example.com")
#         assert new_user.check_password("newpassword")
#
#     def test_user_update(self, api_client, user, superuser):
#         api_client.force_authenticate(user=superuser)
#         url = reverse("users-detail", kwargs={"pk": user.pk})
#         data = {"phone": "+1234567890"}
#         response = api_client.patch(url, data)
#         assert response.status_code == status.HTTP_200_OK
#         user.refresh_from_db()
#         assert user.phone == "+1234567890"
#
#     def test_user_delete(self, api_client, user, superuser):
#         api_client.force_authenticate(user=superuser)
#         url = reverse("users-detail", kwargs={"pk": user.pk})
#         response = api_client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#         assert not User.objects.filter(pk=user.pk).exists()
#
#     def test_user_login(self, api_client, user):
#         url = reverse("login")
#         data = {"email": user.email, "password": "testpassword"}
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_200_OK
#         assert "access" in response.data
#         assert "refresh" in response.data
#
#     def test_user_login_wrong_password(self, api_client, user):
#         url = reverse("login")
#         data = {"email": user.email, "password": "wrongpassword"}
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_user_login_wrong_email(self, api_client):
#         url = reverse("login")
#         data = {"email": "wrong@email.com", "password": "wrongpassword"}
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_401_UNAUTHORIZED
#
#     def test_token_refresh(self, api_client, user):
#         url_login = reverse("login")
#         data_login = {"email": user.email, "password": "testpassword"}
#         response_login = api_client.post(url_login, data_login)
#         refresh_token = response_login.data["refresh"]
#
#         url_refresh = reverse("token_refresh")
#         data_refresh = {"refresh": refresh_token}
#         response_refresh = api_client.post(url_refresh, data_refresh)
#         assert response_refresh.status_code == status.HTTP_200_OK
#         assert "access" in response_refresh.data
#
#     def test_user_create_without_password(self, api_client):
#         url = reverse("register")
#         data = {
#             "email": "newuser2@example.com",
#         }
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#
#     def test_user_create_duplicate_email(self, api_client, user):
#         url = reverse("register")
#         data = {
#             "email": user.email,
#             "password": "newpassword",
#         }
#         response = api_client.post(url, data)
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
