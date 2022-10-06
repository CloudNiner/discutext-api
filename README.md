# DiscuText API

Written with [Flask](https://github.com/pallets/flask/) and deployed with [Zappa](https://github.com/Miserlou/Zappa).

## Getting Started

### Requirements

- Python 3.9
- (Optional) [direnv](https://direnv.net)

For deploying:

Ensure you have an `AWS_PROFILE=discutext-api-zappa-deploy` configured with the appropriate permissions for AWS API Gateway + Lambda + S3.

## Developing

Run `./scripts/setup` to create a virtualenv and install dependencies into it.

If using `direnv`, run `direnv allow`, otherwise activate virtualenv with `source .venv/bin/activate`.

Start the service with `./scripts/server`. The API server will be available at http://localhost:5050

## Deploying

Run `zappa` to deploy:

```bash
zappa update production
```

For initial deployment, instead run `zappa deploy production`.

## Shutting Down

To undeploy the service and cleanup the AWS account:

- `zappa undeploy production`
- Delete AWS API Gateway Custom Domain Name
- Delete AWS CloudFront Distribution for Custom Domain Name
- Delete AWS ACM Certificate in us-east-1
- Delete AWS Route 53 Hosted Zone
