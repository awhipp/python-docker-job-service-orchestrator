'''
Flask Application that provides a REST API for the Swarm Orchestrator
'''
import datetime
import uvicorn

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


from services.docker_service import DockerService
from services.scheduler_service import AsyncScheduler

from routes.job_api import bp as job_api
from routes.service_api import bp as service_api
from routes.image_api import bp as image_api
from routes.scheduler_api import bp as scheduler_api

docker_service: DockerService = DockerService()
scheduler: AsyncScheduler = AsyncScheduler()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.mount('/services/', service_api)
app.mount('/jobs/', job_api)
app.mount('/images/', image_api)
app.mount('/scheduler/', scheduler_api)

@app.get('/')
async def index(request: Request):
    '''
    Renders the index page
    '''

    try:
        # get running services
        services = docker_service.client.services.list()
        for service in services:
            service.attrs['CreatedAt'] = service.attrs['CreatedAt'].split('.')[0].replace('T', ' ')

        # get running jobs
        jobs = docker_service.client.containers.list(all=True)
        for job in jobs:
            if '0001-01-01' in job.attrs['State']['StartedAt']:
                job.runTime = 'Not Started'
                continue
            
            start_time = datetime.datetime.fromisoformat(job.attrs['State']['StartedAt'].split('.')[0] + '.000000+00:00')
            end_time = job.attrs['State']['FinishedAt']
            if '0001-01-01' in end_time:
                # Endtime is now UTC
                end_time = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
            else:
                end_time = datetime.datetime.fromisoformat(end_time.split('.')[0] + '+00:00')
            
            run_time = end_time - start_time
            job.runTime = run_time
            job.attrs['State']['StartedAt'] = job.attrs['State']['StartedAt'].split('.')[0].replace('T', ' ')

        # get all images
        images = docker_service.client.images.list(all=True)
        
        # render HTML template with service data
        return templates.TemplateResponse("services.html", {'request': request, 'services': services, 'jobs': jobs, 'images': images})
    except Exception as exc: # pylint: disable=broad-except
        print(exc)
        return "Error has occured. Please check the logs for more information."

@app.on_event("shutdown")
async def app_shutdown():
    '''
    Shutdown event for the application
    '''
    await scheduler.stop_tasks()

if __name__ == '__main__': 
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, workers=4)
