
from __future__ import annotations

from services.docker_service import DockerService
from services.scheduler_service import AsyncScheduler

from uuid import uuid4
from fastapi import FastAPI, Request, BackgroundTasks

docker_service = DockerService()
scheduler = AsyncScheduler()

bp = FastAPI()

@bp.post('/recurring')
async def recurring_task(request: Request, background_tasks: BackgroundTasks):
    '''
    Add a job to the scheduler
    '''
    request = await request.json()
    print(request)
    task_name = request['task_name']
    image = request['image']
    cron = request['cron']
    job_name = f'{task_name}-{str(uuid4())[:8]}'
    
    background_tasks.add_task(scheduler.schedule_task, task_name, True, cron, docker_service.add_job, job_name, image)
    return {'message': f'Scheduled task: {task_name} successfully at cron: {cron}'}

# TODO: Figure a way to include as a recurring check based on services that request it
# async def scale_services_by_stats():
#     '''
#     Scale services based on stats
#     '''

#     container_stats = {}

#     print('Checking for services to scale')
    
#     # Get Docker Stats for each service running
#     for container in docker_service.client.containers.list(filters={'label': 'com.docker.swarm.service.name'}):
#         name = container.name.split('.')[0]

#         stats = container.stats(stream=False)

#         # CPU %
#         cpu_pct = stats['cpu_stats']['cpu_usage']['total_usage'] / stats['cpu_stats']['system_cpu_usage'] * 100
        
#         # Memory %
#         mem_pct = stats['memory_stats']['usage'] / stats['memory_stats']['limit'] * 100

#         if name not in container_stats:
#             container_stats[name] = {
#                 'max_cpu': 0,
#                 'max_memory': 0,
#                 'count': 0
#             }
        
#         if cpu_pct > container_stats[name]['max_cpu']:
#             container_stats[name]['max_cpu'] = round(cpu_pct, 4)
        
#         if mem_pct > container_stats[name]['max_memory']:
#             container_stats[name]['max_memory'] = round(mem_pct, 4)

#         container_stats[name]['count'] += 1
    
#     print(container_stats)

#     # Loop through and scale up if either memory or cpu is over 80%
#     for service_name, stats in container_stats.items():
#         if stats['max_cpu'] > 80 or stats['max_memory'] > 80:
#             print(f'Service {service_name} has a max CPU of {stats["max_cpu"]}% and a max memory of {stats["max_memory"]}%')
#             print(f'Scaling up {service_name} to {stats["count"] + 1} replicas')
#             docker_service.scale_service(service_name, stats['count'] + 1)