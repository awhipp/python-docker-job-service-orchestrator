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

docker_service: DockerService = DockerService()

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

# TODO: Make non-blocking for reloading the page. Should not affect docker services because those actions are quick.
async def scale_services_by_stats():
    '''
    Scale services based on stats
    '''

    container_stats = {}

    print('Checking for services to scale')
    
    # Get Docker Stats for each service running
    for container in docker_service.client.containers.list(filters={'label': 'com.docker.swarm.service.name'}):
        name = container.name.split('.')[0]

        stats = container.stats(stream=False)

        # CPU %
        cpu_pct = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
        
        # Memory %
        mem_pct = stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100

        if name not in container_stats:
            container_stats[name] = {
                'max_cpu': 0,
                'max_memory': 0,
                'count': 0
            }
        
        if cpu_pct > container_stats[name]['max_cpu']:
            container_stats[name]['max_cpu'] = round(cpu_pct, 4)
        
        if mem_pct > container_stats[name]['max_memory']:
            container_stats[name]['max_memory'] = round(mem_pct, 4)

        container_stats[name]['count'] += 1
    
    print(container_stats)

    # Loop through and scale up if either memory or cpu is over 80%
    for service_name, stats in container_stats.items():
        if stats['max_cpu'] > 80 or stats['max_memory'] > 80:
            print(f'Service {service_name} has a max CPU of {stats["max_cpu"]}% and a max memory of {stats["max_memory"]}%')
            print(f'Scaling up {service_name} to {stats["count"] + 1} replicas')
            docker_service.scale_service(service_name, stats['count'] + 1)
            


async def startup():
    '''
    Startup function for the application
    '''
    scheduler = AsyncScheduler()
    
    # Recurring Task
    scheduler.schedule_task("Scale Service Check", True, "*/1 * * * *",  scale_services_by_stats)

    # One Time Task, 30 seconds in the future
    scheduler.schedule_task("Scheduler Confirmation", False, datetime.datetime.now() + datetime.timedelta(seconds=5), print, f"[{time.ctime()}] Scheduling Service Started.")

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
