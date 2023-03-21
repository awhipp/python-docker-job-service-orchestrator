'''
Flask Application that provides a REST API for the Swarm Orchestrator
'''
from flask import Flask, render_template

from services.docker_service import DockerService

from routes.job_api import bp as job_api
from routes.service_api import bp as service_api

client = DockerService.getInstance().client

app = Flask(__name__)

app.register_blueprint(service_api)
app.register_blueprint(job_api)

@app.route('/')
def index():
    # get running services
    services = client.services.list()
    # render HTML template with service data
    return render_template('services.html', services=services)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
