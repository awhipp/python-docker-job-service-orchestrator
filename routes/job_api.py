'''
Job API
'''

from flask import Blueprint, jsonify, request
from services.docker_service import DockerService

client = DockerService.getInstance().client
bp = Blueprint('job_api', __name__)

@bp.route('/run_job', methods=['POST'])
def run_job():
    '''
    Runs a short-lived job from a container image
    '''
    image = request.json['image']
    job_name = request.json['job_name']
    client.containers.run(image, detach=True, name=job_name)
    return jsonify({'message': 'Job started successfully', 'job_name': job_name}), 201


@bp.route('/monitor_job', methods=['GET'])
def monitor_job():
    '''
    Monitors the state of a short-lived job/container based on container_id
    '''
    job_name = request.args.get('job_name')
    container = client.containers.get(job_name)
    return jsonify({'job_name': job_name, 'state': container.status}), 200

@bp.route('/remove_job', methods=['POST'])
def remove_job():
    '''
    Removes a short-lived job/container based on container_id
    '''
    job_name = request.json['job_name']
    container = client.containers.get(job_name)
    container.remove()
    return jsonify({'message': 'Job removed successfully', 'job_name': job_name}), 200