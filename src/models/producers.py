import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import Producer, db
from flask_jwt_extended import get_jwt_identity, jwt_required
producers = Blueprint("producers",__name__,url_prefix="/api/v1/producers")

@producers.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_producers():
    current_user = get_jwt_identity()
    if request.method == "POST":
        name = request.get_json().get("name", "")
        area = request.get_json().get("area", "")
        
        if Producer.query.filter_by(name=name).first():
            return jsonify({
                "error": "producer already exists."
            }), HTTP_409_CONFLICT

        producer = Producer(
            name = name, 
            area = area
        )

        db.session.add(producer)
        db.session.commit()

        return jsonify({
            "id": producer.id,
            "name": producer.name
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        producers = Producer.query.paginate(page=page, per_page=per_page)
        
        data = []
        for producer in producers.items:
            data.append({
                "id": producer.id,
                "name": producer.name,
                "area": producer.area
            })
        meta = {
            "page": producers.page,
            "pages": producers.pages,
            "total": producers.total,
            "prev_page": producers.prev_num,
            "next_page": producers.next_num,
            "has_next": producers.has_next,
            "has_prev": producers.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@producers.get("/<int:id>")
@jwt_required()
def get_producer(id):
    producer = Producer.query.filter_by(id=id).first()
    if not producer:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "id": producer.id,
        "name": producer.name,
        "area": producer.area
    }), HTTP_200_OK

@producers.put("/<int:id>")
@producers.patch("/<int:id>")
@jwt_required()
def edit_producer(id):
    producer = Producer.query.filter_by(id=id).first()
    if not producer:
        return jsonify({
            "message": "Item not found."
        })
    
    name = request.get_json().get("name", "")
    area = request.get_json().get("area", "")

    producer.name = name
    producer.area = area

    db.session.commit()

    return jsonify({
        "id": producer.id,
        "name": producer.name
    }), HTTP_201_CREATED

@producers.delete("/<int:id>")
@jwt_required()
def delete_producer(id):
    producer = Producer.query.filter_by(id=id).first()
    if not producer:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(producer)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
