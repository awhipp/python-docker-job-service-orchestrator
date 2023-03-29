'''
Flask Application that provides a REST API for the Swarm Orchestrator
'''
import uvicorn
import datetime
import time

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from services.docker_service import DockerService
from services.scheduler_service import AsyncScheduler

from routes.job_api import bp as job_api
from routes.service_api import bp as service_api
from routes.image_api import bp as image_api

client: DockerService = DockerService().client

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
    images = client.images.list(all=True)
    
    # render HTML template with service data
    return templates.TemplateResponse("services.html", {'request': request, 'services': services, 'jobs': jobs, 'images': images})

async def startup():
    '''
    Startup function for the application
    '''
    scheduler = AsyncScheduler()
    print('Scheduling Service Started')
    
    # Recurring Task
    scheduler.schedule_task("Health Check Repeat", True, "*/1 * * * *",  print, f"[{time.ctime()}] Scheduler Healthy (Repeat)")

    # One Time Task, 30 seconds in the future
    scheduler.schedule_task("Health Check Once", False, datetime.datetime.now() + datetime.timedelta(seconds=10), print, f"[{time.ctime()}] Scheduler Healthy (Single)")

    return scheduler

async def shutdown(scheduler: AsyncScheduler):
    '''
    Shutdown function for the application
    '''
    await scheduler.stop_tasks()

@app.on_event("startup")
async def app_startup():
    '''
    Startup event for the application
    '''
    app.scheduler = await startup()

@app.on_event("shutdown")
async def app_shutdown():
    '''
    Shutdown event for the application
    '''
    await shutdown(app.scheduler)

if __name__ == '__main__': 
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True, workers=1)
