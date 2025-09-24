# DiscuText API

Written with [Flask](https://github.com/pallets/flask/) and deployed with [Zappa](https://github.com/Miserlou/Zappa).

## Getting Started

### Requirements

- Python 3.12
- [mise](https://mise.jdx.dev/) tool manager
- [uv](https://docs.astral.sh/uv/) package manager

For deploying:

Ensure you have an `AWS_PROFILE=discutext-api-zappa-deploy` configured with the appropriate permissions for AWS API Gateway + Lambda + S3.

## Developing

Run `./scripts/setup` to initialize the project.

Start the service with `./scripts/server`. The API server will be available at http://localhost:5050

## Docker build

```shell
DISCUTEXT_REGISTRY=...
DISCUTEXT_VERSION=...
docker build --platform linux/amd64 --platform linux/arm64 -t ${DISCUTEXT_REGISTRY}/discutext:latest -t ${DISCUTEXT_REGISTRY}/discutext:${DISCUTEXT_VERSION} .
```

## Deploying

Run `zappa` to deploy:

```bash
uv run zappa update production
```

For initial deployment, instead run `uv run zappa deploy production`.

## Shutting Down

To undeploy the service and cleanup the AWS account:

- `uv run zappa undeploy production`
- Delete AWS API Gateway Custom Domain Name
- Delete AWS CloudFront Distribution for Custom Domain Name
- Delete AWS ACM Certificate in us-east-1
- Delete AWS Route 53 Hosted Zone
