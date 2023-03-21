'''
Singleton class for docker service
'''
import docker

class DockerService:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DockerService.__instance == None:
            DockerService()
        return DockerService.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DockerService.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DockerService.__instance = self
            self.client = docker.from_env()