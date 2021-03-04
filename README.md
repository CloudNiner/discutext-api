# DiscuText API

API serving https://api.discutext.com, written with [Flask](https://github.com/pallets/flask/) and deployed with [Zappa](https://github.com/Miserlou/Zappa).

## Getting Started

### Requirements

- Docker
- Docker Compose v3+

For deploying:

- Python 3
- Virtualenv
- Virtualenvwrapper (optional as a convenience)

Ensure you have an `AWS_PROFILE=discutext` configured with the appropriate permissions for AWS API Gateway + Lambda + S3.

## Developing

Start API container with:

```bash
docker-compose up
```

The API server will be available at http://localhost:5050

## Deploying

Create or activate a virtualenv and ensure dependencies are up to date:

```bash
mkvirtualenv --python python3.7 discutext
# OR
workon discutext

pip3 install -r requirements.txt
```

Then run `zappa` to deploy:

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

