'''
Service API
'''

from flask import Blueprint, jsonify, request
from services.docker_service import DockerService

client = DockerService.getInstance().client
bp = Blueprint('service_api', __name__)


@bp.route('/add_service', methods=['POST'])
def add_service():
    '''
    Adds a long-running service from a container image
    '''
    service_name = request.json['service_name']
    image = request.json['image']
    # create service
    service = client.services.create(image, name=service_name)
    return jsonify({'message': 'Service created successfully', 'service_id': service.id}), 201


@bp.route('/scale_service', methods=['POST'])
def scale_service():
    '''
    Scales a long-running service based on service_id
    '''
    service_name = request.json['service_name']
    replicas = request.json['replicas']
    service = client.services.list(filters={'name': service_name})[0]
    service.scale(replicas=replicas)
    return jsonify({'message': 'Service scaled successfully', 'service_name': service_name}), 200


@bp.route('/remove_service', methods=['POST'])
def remove_service():
    '''
    Removes a long-running service based on service name
    '''
    service_name = request.json['service_name']
    service = client.services.list(filters={'name': service_name})[0]
    service.remove()
    return jsonify({'message': 'Service removed successfully', 'service_name': service_name}), 200


@bp.route('/monitor_service', methods=['GET'])
def monitor_service():
    '''
    Monitors the state of a long-running service based on service_id
    '''
    service_name = request.args.get('service_name')
    service = client.services.list(filters={'name': service_name})[0]
    service_tasks = service.tasks()
    task_states = []
    for task in service_tasks:
        task_states.append({'id': task.id, 'state': task.status['State']})
    return jsonify({'service_name': service_name, 'tasks': task_states}), 200