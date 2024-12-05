from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import shortuuid

# Import the app, db, and migrate from your config file
from config import app, db, migrate

# Import your models here
from models import User, Build, Perk, Vote  # Ensure Vote is imported

def load_perks():
    perks_file_path = os.path.join(os.path.dirname(__file__), 'perks.json')
    with open(perks_file_path, 'r') as file:
        perks_data = json.load(file)
        for perk in perks_data:
            existing_perk = Perk.query.filter_by(name=perk['name']).first()
            if not existing_perk:
                new_perk = Perk(name=perk['name'], image=perk['image'])
                db.session.add(new_perk)
        db.session.commit()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    new_user = User(username=username, email=email, password_hash=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user': {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Login successful', 'user': {'id': user.id, 'username': user.username, 'email': user.email}}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/builds', methods=['POST'])
def create_build():
    data = request.json
    user_id = data['user_id']
    perks = data['perks']
    folder_path = data.get('folder_path')  # Get the folder path from the request

    new_build = Build(user_id=user_id, folder_path=folder_path)  # Store the folder path
    db.session.add(new_build)
    db.session.commit()

    for perk_data in perks:
        perk = Perk.query.get(perk_data['id'])
        if perk and perk not in new_build.perks:
            new_build.perks.append(perk)
        elif not perk:
            return jsonify({'message': f'Perk with id {perk_data["id"]} not found'}), 404

    db.session.commit()

    return jsonify({'message': 'Build created successfully', 'build': {'id': new_build.id, 'user_id': new_build.user_id, 'folder_path': new_build.folder_path, 'perks': [{'id': perk.id, 'name': perk.name, 'image': perk.image} for perk in new_build.perks]}}), 201

@app.route('/api/builds', methods=['GET'])
def get_builds():
    builds = Build.query.all()
    builds_data = []
    for build in builds:
        build_data = {
            'id': build.id,
            'user_id': build.user_id,
            'folder_path': build.folder_path,
            'priority': build.priority,
            'perks': [{'id': perk.id, 'name': perk.name, 'image': perk.image} for perk in build.perks]
        }
        builds_data.append(build_data)
    return jsonify(builds_data)

@app.route('/api/builds/<int:build_id>', methods=['DELETE'])
def delete_build(build_id):
    build = Build.query.get(build_id)
    if not build:
        return jsonify({'message': 'Build not found'}), 404

    db.session.delete(build)
    db.session.commit()

    return jsonify({'message': 'Build deleted successfully'}), 200

@app.route('/api/builds/<int:build_id>', methods=['PUT'])
def update_build(build_id):
    data = request.json
    build = Build.query.get(build_id)
    if not build:
        return jsonify({'message': 'Build not found'}), 404

    build.perks = []
    for perk_data in data['perks']:
        perk = Perk.query.get(perk_data['id'])
        if perk:
            build.perks.append(perk)
        else:
            return jsonify({'message': f'Perk with id {perk_data["id"]} not found'}), 404

    db.session.commit()

    return jsonify({'message': 'Build updated successfully', 'build': {'id': build.id, 'user_id': build.user_id, 'folder_path': build.folder_path, 'perks': [{'id': perk.id, 'name': perk.name, 'image': perk.image} for perk in build.perks]}}), 200

@app.route('/api/builds/<int:build_id>/code', methods=['POST'])
def save_build_code(build_id):
    data = request.json
    build = Build.query.get(build_id)
    if not build:
        return jsonify({'message': 'Build not found'}), 404

    build.code = data['code']
    db.session.commit()

    return jsonify({'message': 'Code saved successfully'}), 200

@app.route('/api/builds/<int:build_id>/vote', methods=['POST'])
def vote_build(build_id):
    data = request.json
    vote_type = data['vote_type']
    user_id = data['user_id']

    build = Build.query.get(build_id)
    if not build:
        return jsonify({'message': 'Build not found'}), 404

    if vote_type == 'up':
        build.priority += 1
    elif vote_type == 'down':
        build.priority -= 1
    else:
        return jsonify({'message': 'Invalid vote type'}), 400

    db.session.commit()

    return jsonify({'message': 'Vote recorded', 'priority': build.priority}), 200

@app.route('/api/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    builds = Build.query.filter_by(user_id=user_id).all()
    votes = Vote.query.filter_by(user_id=user_id).count()
    builds_data = []
    for build in builds:
        build_data = {
            'id': build.id,
            'folder_path': build.folder_path,
            'priority': build.priority,
            'perks': [{'id': perk.id, 'name': perk.name, 'image': perk.image} for perk in build.perks]
        }
        builds_data.append(build_data)

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'builds': builds_data,
        'votes': votes
    })

@app.route('/api/perks', methods=['GET'])
def get_perks():
    perks = Perk.query.all()
    perks_data = [{'id': perk.id, 'name': perk.name, 'image': perk.image} for perk in perks]
    return jsonify(perks_data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_perks()
    app.run(host='0.0.0.0', port=5000, debug=True)