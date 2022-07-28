import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import Task, db
from flask_jwt_extended import get_jwt_identity, jwt_required
tasks = Blueprint("tasks",__name__,url_prefix="/api/v1/tasks")

@tasks.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_tasks():
    current_user = get_jwt_identity()
    if request.method == "POST":
        type_id = request.get_json().get("type_id", "")
        project_id = request.get_json().get("project_id", "")
        producer_id = request.get_json().get("producer_id", "")
        description = request.get_json().get("description", "")
        deadline = request.get_json().get("deadline", "")

        if Task.query.filter_by(project_id = project_id, type_id=type_id, deadline=deadline).first():
            return jsonify({
                "error": "task already exists."
            }), HTTP_409_CONFLICT

        task = Task(
            type_id = type_id, 
            project_id = project_id,
            producer_id = producer_id,
            description = description,
            deadline = deadline
        )

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "id": task.id,
            "description": task.description
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        tasks = Task.query.paginate(page=page, per_page=per_page)
        
        data = []
        for task in tasks.items:
            data.append({
                "id": task.id,
                "description": task.description
            })
        meta = {
            "page": tasks.page,
            "pages": tasks.pages,
            "total": tasks.total,
            "prev_page": tasks.prev_num,
            "next_page": tasks.next_num,
            "has_next": tasks.has_next,
            "has_prev": tasks.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@tasks.get("/<int:id>")
@jwt_required()
def get_task(id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "id": task.id,
        "description": task.description
    }), HTTP_200_OK

@tasks.put("/<int:id>")
@tasks.patch("/<int:id>")
@jwt_required()
def edit_task(id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        return jsonify({
            "message": "Item not found."
        })
    
    type_id = request.get_json().get("type_id", "")
    project_id = request.get_json().get("project_id", "")
    producer_id = request.get_json().get("producer_id", "")
    description = request.get_json().get("description", "")
    deadline = request.get_json().get("deadline", "")

    task.type_id = type_id
    task.project_id = project_id
    task.producer_id = producer_id
    task.description = description
    task.deadline = deadline

    db.session.commit()

    return jsonify({
        "id": task.id,
        "name": task.description
    }), HTTP_201_CREATED

@tasks.delete("/<int:id>")
@jwt_required()
def delete_task(id):
    task = Task.query.filter_by(id=id).first()
    if not task:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(task)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
