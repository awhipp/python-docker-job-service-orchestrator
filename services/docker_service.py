'''
Singleton class for docker service
'''
import docker

class DockerService:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        DockerService.__instance = self
        self.client = docker.from_env()

    def add_image(self, image_name: str, image_version: str):
        '''
        Add a container image to the local docker registry
        '''

        print(f'Adding image: [{image_name}:{image_version}]')

        image = None
        if image_version == '':
            image = self.client.images.pull(f"{image_name}")
        else:
            image = self.client.images.pull(f"{image_name}:{image_version}")
            
        return {'message': 'Image added successfully', 'image': image.attrs['RepoTags'][0]}
    
    def remove_image(self, image_name: str):
        '''
        Remove a container image from the local docker registry
        '''

        print(f'Removing image: [{image_name}]')

        image = self.client.images.get(f"{image_name}")
        image_removed = image.attrs['RepoTags'][0]

        try:
            self.client.images.remove(image.id, force=True)
            return {'message': f'Successfully removed {image_removed}'}
        except docker.errors.APIError:
            return {'message': f'Unable to remove {image_removed}. Is there a job or service running?'}

    def add_job(self, job_name: str, image: str):
        '''
        Add a job to the docker swarm
        '''
        print(
            f"Running job: [{job_name}] from image: [{image}]"
        )

        self.client.containers.run(image, detach=True, name=job_name)
        return {'message': 'Job started successfully', 'job_name': job_name}
    
    def remove_job(self, job_name: str):
        '''
        Remove a job from the docker swarm
        '''
        print(
            f"Removing job: [{job_name}]"
        )
        container = self.client.containers.get(job_name)
        container.remove(force=True)
        return {'message': 'Job removed successfully', 'job_name': job_name}
    
    # TODO: Use since, until to paginate since last request and append
    def get_job_logs(self, job_name: str):
        container = self.client.containers.get(job_name)
        logs = container.logs(tail='all', stdout=True, stderr=True)
        logs = logs.decode('utf-8')
        return {'message': 'Job logs retrieved successfully', 'job_name': job_name, 'logs': logs}
    

    def add_service(self, service_name: str, image: str):
        '''
        Add a service to the docker swarm
        '''
        print(
            f"Running service: [{service_name}] from image: [{image}]"
        )

        self.client.services.create(image, name=service_name)
        return {'message': 'Service started successfully', 'service_name': service_name}
    
    def scale_service(self, service_name: str, replicas: int):
        '''
        Scale a service
        '''
        service = self.client.services.list(filters={'name': service_name})[0]
        service.scale(replicas=replicas)
        return {'message': 'Service scaled successfully', 'service_name': service_name, 'replicas': replicas}

    def remove_service(self, service_name: str):
        '''
        Remove a service from the docker swarm
        '''
        print(
            f"Removing service: [{service_name}]"
        )
        service = self.client.services.list(filters={'name': service_name})[0]
        service.remove()
        return {'message': 'Service removed successfully', 'service_name': service_name}
    
    def get_service_logs(self, service_name: str):
        service = self.client.services.list(filters={'name': service_name})[0]
        log_generator = service.logs(since=0, stdout=True, stderr=True)
        logs = ''.join([log.decode('utf-8') for log in log_generator])
        return {'message': 'Service logs retrieved successfully', 'service_name': service_name, 'logs': logs}