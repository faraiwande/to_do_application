# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.8+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.



You'll need to install pytest which is a dependecy that we will use to run the testing suite


```bash
$ poetry add  pytest # 
```

Execute the command above & it should download pytest & also update the pyproject.toml as well.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Connecting To Trello

You need to create an account in Trello & obtained a TRELLO_API_KEY & TRELLO_API_TOKEN. 

- SIGN UP https://trello.com/signup

- AUTH https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/#managing-your-api-key


## Ansible for Deployment of Application
You will need to deploy the application using Ansible you need to copy the `ansible` folder to the Host Node. Update the inventory file with the control nodes you want to deploy to & then run the following command:

```bash
ansible-playbook playbook.yaml -i inventory.yaml
```
> You must setup passwordless SSH Access from the Host to your Control Nodes


## To run the container for local development, please run
```bash
docker run --env-file ./.env -p 5100:5000 --mount "type=bind,source=$(pwd)/todo_app,target=/app/todo_app" -it todo_app:dev
```

## The build & run commands for prod are : 
```bash

docker build --target prod --tag todo_app:prod -f dockerfiles/Dockerfile.todo_app .

docker run --publish 8000:5000 -it --env-file .env todo_app:prod 


```

## Architecture Diagrams
Diagrams are in the in the '`diagrams` subfolder. You can use the `.drawoi` file to edit the diagrams, which were built using [app.diagrams.net](app.diagrams.net).
=======
## Building & Running the App via Docker
To build the container for local development, please run 
```bash
docker build --target dev --tag todo_app:dev -f dockerfiles/Dockerfile.todo_app .
```
