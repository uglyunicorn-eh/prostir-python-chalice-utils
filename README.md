# Python Utils for AWS Chalice

`chalice_utils` is a set of tools and helpers for [AWS Chalice](https://github.com/aws/chalice)

## Requirements

* Python 3.9
* [chalice](https://github.com/aws/chalice)

## Features

* [Graphene](https://graphene-python.org) GraphQL Server support
* [AWS CloudWatch](https://aws.amazon.com/cloudwatch/) logs formatter
* [Sentry](https://sentry.io/) integration

## Development

### Testing

* create a virtual environment `.env` and activate it
* install testing dependencies: `pip install -e ".[develop]"`
* run `make test`

### Building docs

* install testing dependencies: `pip install -e ".[docs]"`
* run `make docs`

## Change Log

**Version 0.0.1**

* Basic graphene support
* Basic CloudWatch logs formatter
* Sentry integration
