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
    
    def scale_service(self, service_name: str, replicas: int):
        '''
        Scale a service
        '''
        service = self.client.services.get(service_name)
        service.scale(replicas=replicas)