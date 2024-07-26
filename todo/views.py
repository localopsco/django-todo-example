from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
import boto3
import json
from botocore.exceptions import NoCredentialsError
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from django.http import JsonResponse


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        url_path="attach",
        parser_classes=[MultiPartParser],
    )
    def attach(self, request, pk=None):
        if not settings.S3_ENABLED:
            return JsonResponse({
                "message": "Attachments feature not enabled"
            }, status=403)

        task = self.get_object()
        file = request.FILES["file"]

        s3 = boto3.client(
            "s3",
            region_name=settings.S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        try:
            s3.upload_fileobj(file, settings.S3_BUCKET_NAME, file.name)
            task.attachment_url = (
                f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{file.name}"
            )
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NoCredentialsError:
            return Response(
                {"message": "Credentials not available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=["delete"], url_path="attach")
    def delete_attachment(self, request, pk=None):
        if not settings.S3_ENABLED:
            return JsonResponse({
                "message": "Attachments feature not enabled"
            }, status=403)

        task = self.get_object()
        if not task.attachment_url:
            return Response(
                {"message": "No attachment to delete"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        s3 = boto3.client(
            "s3",
            region_name=settings.S3_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        try:
            # Extract the file name from the attachment URL
            file_name = task.attachment_url.split("/")[-1]
            s3.delete_object(Bucket=settings.S3_BUCKET_NAME, Key=file_name)
            task.attachment_url = None
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NoCredentialsError:
            return Response(
                {"message": "Credentials not available"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ClientError as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def meta_resp(request):
    cloud_deps = []
    attachment_supported = False

    if settings.S3_ENABLED:
        cloud_deps.append("AWS S3")
        attachment_supported = True

    data = {
        "framework": "django",
        "version": settings.APP_VERSION,
        "stack": "Django, Postgres, Redis, React.JS",
        "cloud_dependencies": ", ".join(cloud_deps),
        "attachment_supported": attachment_supported,
    }
    return JsonResponse(data)


def health(request):
    data = {
        "status": "ok",
    }
    return JsonResponse(data)

def lops_helm_values(request):
    lops_helm_values = {}
    try:
      lops_helm_values = json.loads(settings.LOPS_HELM_VALUES)
      if lops_helm_values is None:
        lops_helm_values = {}
    except ValueError as e:
      return Response(
              {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
          )
    return JsonResponse(lops_helm_values, safe=False)
