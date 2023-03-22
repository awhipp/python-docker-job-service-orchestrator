'''
Job API
'''

import re
from uuid import uuid4
from flask import Blueprint, jsonify, request
from services.docker_service import DockerService

client = DockerService.getInstance().client
bp = Blueprint('job_api', __name__)

@bp.route('/run_job', methods=['POST'])
def run_job():
    '''
    Runs a short-lived job from a container image
    '''
    job_name = " ".join(request.json['job_name'].strip().split())
    job_name = re.sub(r'[^a-zA-Z0-9]', '_', job_name)
    job_name = f"{job_name}-{str(uuid4())[:8]}"
    image = request.json['image'].strip() # Image Name or Image ID

    print(
        f"Running job: [{job_name}] from image: [{image}]"
    )

    client.containers.run(image, detach=True, name=job_name)
    return jsonify({'message': 'Job started successfully', 'job_name': job_name}), 201

@bp.route('/remove_job', methods=['POST'])
def remove_job():
    '''
    Removes a short-lived job/container based on container_id
    '''
    job_name = request.json['job_name']
    container = client.containers.get(job_name)
    container.stop()
    container.remove(force=True)
    return jsonify({'message': 'Job removed successfully', 'job_name': job_name}), 200
