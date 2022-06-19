# DiscuText API

Written with [Flask](https://github.com/pallets/flask/) and deployed with [Zappa](https://github.com/Miserlou/Zappa).

## Getting Started

### Requirements

- Python 3
- (Optional) [direnv](https://direnv.net)

For deploying:

Ensure you have an `AWS_PROFILE=discutext` configured with the appropriate permissions for AWS API Gateway + Lambda + S3.

## Developing

Run `./scripts/setup` to create a virtualenv and install dependencies into it.

If using `direnv`, run `direnv allow`, otherwise activate virtualenv with `source .venv/bin/activate`.

Start the service with `python3 app.py`. The API server will be available at http://localhost:5050

## Deploying

Run `zappa` to deploy:

```bash
zappa update production
```

## Service Shutdown

Shutdown this service in March 2021 because Reader Mode on my iPad now formats the forecast discussions nicely.

The following actions were taken:

- `zappa undeploy production`
- Deleted AWS ACM Certificate
- Deleted AWS Route 53 Hosted Zone
- Deleted mailgun account
- Cancelled domain autorenewal
