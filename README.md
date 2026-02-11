# DiscuText API

Written with [Flask](https://github.com/pallets/flask/) and deployed with [Zappa](https://github.com/Miserlou/Zappa).

## Getting Started

### Requirements

- [mise](https://mise.jdx.dev/) tool manager

For deploying:

Ensure you have an `AWS_PROFILE=discutext-api-zappa-deploy` configured with the appropriate permissions for AWS API Gateway + Lambda + S3.

## Developing

Run `./scripts/setup` to initialize the project.

Run `./scripts/test` to run linting, formatting, and type checking.

Start the service with `./scripts/server`. The API server will be available at http://localhost:5050

## Docker build

```shell
DISCUTEXT_REGISTRY=...
DISCUTEXT_VERSION=...
docker build --platform linux/amd64 --platform linux/arm64 -t ${DISCUTEXT_REGISTRY}/discutext:latest -t ${DISCUTEXT_REGISTRY}/discutext:${DISCUTEXT_VERSION} .
```

## Deploying

Run `./scripts/update` to update the existing deployment.

For initial deployment, instead run `zappa deploy production`.

## Shutting Down

To undeploy the service and cleanup the AWS account:

- `zappa undeploy production`
- Delete AWS API Gateway Custom Domain Name
- Delete AWS CloudFront Distribution for Custom Domain Name
- Delete AWS ACM Certificate in us-east-1
- Delete AWS Route 53 Hosted Zone
