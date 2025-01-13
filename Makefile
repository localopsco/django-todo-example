# get value from args if private or public

registry-url=public.ecr.aws/r5p6q2u1

ecr-repo-name=django-todo-be
helm-repo-name=django-todo-example-helm

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
	aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin ${registry-url}

be-docker-push: login
	docker buildx build --platform linux/amd64 -t ${ecr-repo-name}:latest -t ${ecr-repo-name}:${v} .
	docker tag ${ecr-repo-name}:latest ${ecr-repo-url}:latest
	docker tag ${ecr-repo-name}:${v} ${ecr-repo-url}:${v}
	docker push ${ecr-repo-url}:latest
	docker push ${ecr-repo-url}:${v}


login-helm:
	aws ecr get-login-password --region us-west-1 | helm registry login --username AWS --password-stdin ${registry-url}

deploy-helm: login-helm
	helm package helm -d helm/.tmp/
	helm push helm/.tmp/${helm-repo-name}-${v}.tgz oci://${registry-url}
