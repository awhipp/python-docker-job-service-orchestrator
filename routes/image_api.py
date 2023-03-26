'''
Image API
'''
from __future__ import annotations

from docker.errors import APIError
from fastapi import FastAPI, Request
from services.docker_service import DockerService

client = DockerService.getInstance().client
bp = FastAPI()

@bp.post('/add')
async def add_image(request: Request):
    '''
    Add a container image to the local docker registry
    '''
    request = await request.json()
    image_name = " ".join(request['image_name'].strip().split())
    image_version = " ".join(request['image_version'].strip().split())

    image = None
    if image_version == '':
        image = client.images.pull(f"{image_name}")
    else:
        image = client.images.pull(f"{image_name}:{image_version}")

    return {'message': 'Image added successfully', 'image': image.attrs['RepoTags'][0]}

@bp.post('/remove')
async def remove_image(request: Request):
    '''
    Add a container image to the local docker registry
    '''
    request = await request.json()
    image_name = " ".join(request['image_name'].strip().split())
    
    image = client.images.get(f"{image_name}")
    image_removed = image.attrs['RepoTags'][0]

    try:
        client.images.remove(image.id, force=True)
        return {'message': f'Successfully removed {image_removed}'}
    except APIError:
        return {'message': f'Unable to remove {image_removed}. Is there a job or service running?'}
