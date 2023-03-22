'''
Flask Application that provides a REST API for the Swarm Orchestrator
'''
import datetime

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
    '''
    Renders the index page
    '''
    # get running services
    services = client.services.list()
    for service in services:
        service.attrs['CreatedAt'] = service.attrs['CreatedAt'].split('.')[0].replace('T', ' ')

    # get running jobs
    jobs = client.containers.list(all=True)
    for job in jobs:
        if '0001-01-01' in job.attrs['State']['StartedAt']:
            job.runTime = 'Not Started'
            continue
        
        startTime = datetime.datetime.fromisoformat(job.attrs['State']['StartedAt'].split('.')[0] + '.000000+00:00')
        endTime = job.attrs['State']['FinishedAt']
        if '0001-01-01' in endTime:
            # Endtime is now UTC
            endTime = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
        else:
            endTime = datetime.datetime.fromisoformat(endTime.split('.')[0] + '+00:00')
        
        runTime = endTime - startTime
        job.runTime = runTime
        job.attrs['State']['StartedAt'] = job.attrs['State']['StartedAt'].split('.')[0].replace('T', ' ')

    # render HTML template with service data
    return render_template('services.html', services=services, jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
