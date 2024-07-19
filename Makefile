run:
	DB_NAME=djangotodo \
	DB_USER=localops \
	DB_PASS=localops \
	DB_HOST=localhost \
	DB_PORT=5432 \
	S3_BUCKET_NAME=djangotodo \
	S3_REGION=ap-south-1 \
	AWS_ACCESS_KEY_ID=fake-access-key-id \
	AWS_SECRET_ACCESS_KEY=fake-secret-access-key \
	S3_BUCKET_NAME=djangotodo \
	python manage.py runserver

test:
	DB_NAME=djangotodo \
	DB_USER=localops \
	DB_PASS=localops \
	DB_HOST=localhost \
	DB_PORT=5432 \
	S3_BUCKET_NAME=djangotodo \
	S3_REGION=ap-south-1 \
	AWS_ACCESS_KEY_ID=fake-access-key-id \
	AWS_SECRET_ACCESS_KEY=fake-secret-access-key \
	S3_BUCKET_NAME=test-bucket \
	python manage.py test todo

be-docker-push:
	docker buildx build --platform linux/amd64 -t django-todo-be:latest -t django-todo-be:${v} .
	docker tag django-todo-be:latest public.ecr.aws/r5p6q2u1/django-todo-be:latest
	docker tag django-todo-be:${v} public.ecr.aws/r5p6q2u1/django-todo-be:${v}
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/r5p6q2u1
	docker push public.ecr.aws/r5p6q2u1/django-todo-be:latest
	docker push public.ecr.aws/r5p6q2u1/django-todo-be:${v}

deploy-helm:
	helm package helm -d helm/.tmp/
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/r5p6q2u1
	helm push helm/.tmp/django-todo-example-helm-${v}.tgz oci://public.ecr.aws/r5p6q2u1/
