#!/usr/bin/env python

from flask import Flask, request, jsonify
from deployment import create, verify_json_keys, get_deployment_info, get_all_deployments, create_postgresql_deployment
import json

app = Flask(__name__)

@app.route('/create', methods=['POST'])
def process_create():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        check_passed = verify_json_keys(data)
        if not check_passed:
            return jsonify({'error': 'Bad JSON data'}), 400

        create(data)

        return jsonify({'message': 'Data processed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_dep_info', methods=['POST'])
def process_get_dep_info():
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'No JSON data received or missing "name" field'}), 400

        deployment_name = data['name']
        deployment_info = get_deployment_info(deployment_name)

        return deployment_info, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_all_deps', methods=['POST'])
def process_get_all_deps():
    try:
        all_deployment_info = get_all_deployments()

        return all_deployment_info, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deploy-postgresql', methods=['POST'])
def deploy_postgresql():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        required_fields = ['AppName', 'Resources', 'External']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        app_name = data['AppName']
        replicas = 1
        image = 'postgres:13.4'
        secret_name = 'postgresql-credentials'
        resources = data['Resources']
        external = data.get('External', False)

        result = create_postgresql_deployment("default", app_name, replicas, image, secret_name, resources, external)
        return jsonify({'message': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/make_cronjob', methods=['POST'])
def make_the_cronjob():
    try:
        all_deployment_info = get_all_deployments()

        return all_deployment_info, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
