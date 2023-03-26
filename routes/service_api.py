'''
Service API
'''

import re
from uuid import uuid4
from flask import Blueprint, jsonify, request
from services.docker_service import DockerService

client = DockerService.getInstance().client
bp = Blueprint('service_api', __name__)


@bp.route('/add_service', methods=['POST'])
def add_service():
    '''
    Adds a long-running service from a container image
    '''
    service_name = " ".join(request.json['service_name'].strip().split())
    service_name = re.sub(r'[^a-zA-Z0-9]', '_', service_name)
    service_name = f"{service_name}-{str(uuid4())[:8]}"
    image = request.json['image'].strip() # Image Name or Image ID

    print(f"Adding service: [{service_name}] from image: [{image}]")

    # create service
    service = client.services.create(image, name=service_name)
    return jsonify({'message': 'Service created successfully', 'service_name': service.name}), 201


@bp.route('/scale_service', methods=['PUT'])
def scale_service():
    '''
    Scales a long-running service based on service_id
    '''
    service_name = request.json['service_name']
    replicas = int(request.json['replicas'])
    service = client.services.list(filters={'name': service_name})[0]
    service.scale(replicas=replicas)
    return jsonify({'message': 'Service scaled successfully', 'service_name': service_name, 'replicas': replicas}), 200

@bp.route('/remove_service', methods=['POST'])
def remove_service():
    '''
    Removes a long-running service based on service name
    '''
    service_name = request.json['service_name']
    print(service_name)
    service = client.services.list(filters={'name': service_name})[0]
    service.remove()
    return jsonify({'message': 'Service removed successfully', 'service_name': service_name}), 200

# TODO: Use since, until to paginate since last request and append
@bp.route('/get_service_logs', methods=['POST'])
def get_service_logs():
    '''
    Get logs from a long-running service based on service name
    '''
    service_name = request.json['service_name']
    service = client.services.list(filters={'name': service_name})[0]
    log_generator = service.logs(since=0, stdout=True, stderr=True)
    logs = ''.join([log.decode('utf-8') for log in log_generator])
    return jsonify({'message': 'Service logs retrieved successfully', 'service_name': service_name, 'logs': logs}), 200