# get value from args if private or public

registry-url=public.ecr.aws/r5p6q2u1

ecr-repo-name=django-todo-be
helm-repo-name=django-todo-example-helm
aws-repo-region=us-east-1

ecr-repo-url=${registry-url}/${ecr-repo-name}

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

login:
	aws ecr-public get-login-password --region ${aws-repo-region} | docker login --username AWS --password-stdin ${registry-url}

be-docker-push: login
	docker buildx build --push --provenance=false --platform linux/amd64,linux/arm64 \
		-t ${ecr-repo-url}:${v} \
		-t ${ecr-repo-url}:latest .

login-helm:
	aws ecr-public get-login-password --region ${aws-repo-region} | helm registry login --username AWS --password-stdin ${registry-url}

deploy-helm: login-helm
	helm package helm -d helm/.tmp/
	helm push helm/.tmp/${helm-repo-name}-${v}.tgz oci://${registry-url}
