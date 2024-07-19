from moto import mock_aws
import boto3
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import Task
from django.conf import settings
import uuid


class TaskFileUploadTestCase(APITestCase):
    @mock_aws
    def setUp(self):
        self.client = APIClient()
        self.task = Task.objects.create(
            title="Implement example app",
            description="Write helm example app to seed in customer accounts to demonstrate the capabilities of our platform",
            is_completed=False
        )
        self.base_url = reverse('task-list')

    def test_create_task(self):
        url = self.base_url
        data = {
            "title": "New Task",
            "description": "Description for new task",
            "is_completed": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])

    def test_update_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "is_completed": True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertTrue(response.data['is_completed'])

    def test_get_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_list_tasks(self):
        url = self.base_url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_delete_task(self):
        url = reverse('task-detail', kwargs={'pk': self.task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    @mock_aws
    def test_upload_file_to_task(self):
        # Mock S3 setup
        self.s3 = boto3.client('s3', region_name=settings.S3_REGION, aws_access_key_id='fake_access_key', aws_secret_access_key='fake_secret_key')
        self.s3.create_bucket(Bucket=settings.S3_BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': settings.S3_REGION})

        url = reverse('task-attach', kwargs={'pk': self.task.id})

        # Create a simple uploaded file
        file = SimpleUploadedFile("test_file.png", b"file_content", content_type="image/png")

        # Perform the file upload
        response = self.client.post(url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('attachment_url', response.data)
        self.assertTrue(response.data['attachment_url'].startswith(f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com"))
