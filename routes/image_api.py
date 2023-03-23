'''
Image API
'''
from docker.errors import APIError
from flask import Blueprint, jsonify, request
from services.docker_service import DockerService

client = DockerService.getInstance().client
bp = Blueprint('image_api', __name__)

@bp.route('/add_image', methods=['POST'])
def add_image():
    '''
    Add a container image to the local docker registry
    '''
    image_name = " ".join(request.json['image_name'].strip().split())
    image_version = " ".join(request.json['image_version'].strip().split())

    image = None
    if image_version == '':
        image = client.images.pull(f"{image_name}")
    else:
        image = client.images.pull(f"{image_name}:{image_version}")

    return jsonify({'message': 'Image added successfully', 'image': image.attrs['RepoTags'][0]}), 201

@bp.route('/remove_image', methods=['POST'])
def remove_image():
    '''
    Add a container image to the local docker registry
    '''
    image_name = " ".join(request.json['image_name'].strip().split())
    
    image = client.images.get(f"{image_name}")
    image_removed = image.attrs['RepoTags'][0]

    try:
        client.images.remove(image.id, force=True)
        return jsonify({'message': f'Successfully removed {image_removed}'}), 201
    except APIError:
        return jsonify({'message': f'Unable to remove {image_removed}. Is there a job or service running?'}), 500