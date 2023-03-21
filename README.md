# Flask Python Job and Service Orchestrator

## Introduction

This is a simple Flask application that allows you to run jobs and services on a Docker Swarm cluster. It is a simple wrapper around the Docker API.

## Installation

### Requirements

* Docker
* Docker Swarm
* Python 3.8+
* Poetry

### Setup

1. Clone the repository
2. Initialize docker swarm with `docker swarm init`
3. Run `poetry install` to install the dependencies
4. Run `poetry shell` to activate the virtual environment
5. Run `python app.py` to start the application
6. Execute API calls based on what jobs and services you want to run

## API

### Jobs

Jobs are one-off tasks that are run on the Docker Swarm cluster. They are not persistent and are not meant to be run continuously.

#### Services

Services are persistent tasks that are run on the Docker Swarm cluster. They are meant to be run continuously and replicated if needed.