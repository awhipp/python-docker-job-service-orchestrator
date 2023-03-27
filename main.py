'''
Flask Application that provides a REST API for the Swarm Orchestrator
'''
import uvicorn
import datetime

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from services.docker_service import DockerService
from services.scheduler_service import Scheduler

from routes.job_api import bp as job_api
from routes.service_api import bp as service_api
from routes.image_api import bp as image_api

client: DockerService = DockerService.getInstance().client

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount('/services/', service_api)
app.mount('/jobs/', job_api)
app.mount('/images/', image_api)

@app.get('/')
async def index(request: Request):
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

    # get all images
    images = client.images.list(all=True)
    
    # render HTML template with service data
    return templates.TemplateResponse("services.html", {'request': request, 'services': services, 'jobs': jobs, 'images': images})

if __name__ == '__main__':

    # Scheduler start before first request
    @app.on_event("startup")
    def startup_event():
        scheduler: Scheduler = Scheduler.getInstance()
        
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, workers=1)
