import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import Customer, db
from flask_jwt_extended import get_jwt_identity, jwt_required
customers = Blueprint("customers",__name__,url_prefix="/api/v1/customers")

@customers.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_customers():
    current_user = get_jwt_identity()
    if request.method == "POST":
        name = request.get_json().get("name", "")
        email = request.get_json().get("email", "")
        phone_num = request.get_json().get("phone_num", "")
        #checks if email is valid
        if not validators.email(email):
            return jsonify({
                "error": "Email is invalid."
            }), HTTP_400_BAD_REQUEST

        if Customer.query.filter_by(name=name).first():
            return jsonify({
                "error": "Customer already exists."
            }), HTTP_409_CONFLICT

        Customer = Customer(
            name = name, 
            phone_num = phone_num,
            email = email
        )

        db.session.add(Customer)
        db.session.commit()

        return jsonify({
            "id": Customer.id,
            "name": Customer.name
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        customers = Customer.query.paginate(page=page, per_page=per_page)
        
        data = []
        for Customer in customers.items:
            data.append({
                "name": Customer.name,
                "email": Customer.email,
                "phone_num": Customer.phone_num
            })
        meta = {
            "page": customers.page,
            "pages": customers.pages,
            "total": customers.total,
            "prev_page": customers.prev_num,
            "next_page": customers.next_num,
            "has_next": customers.has_next,
            "has_prev": customers.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@customers.get("/<int:id>")
@jwt_required()
def get_Customer(id):
    customer = Customer.query.filter_by(id=id).first()
    if not customer:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "name": customer.name,
        "email": customer.email,
        "phone_num": customer.phone_num
    }), HTTP_200_OK

@customers.put("/<int:id>")
@customers.patch("/<int:id>")
@jwt_required()
def edit_customer(id):
    customer = Customer.query.filter_by(id=id).first()
    if not Customer:
        return jsonify({
            "message": "Item not found."
        })
    
    name = request.get_json().get("name", "")
    email = request.get_json().get("email", "")
    phone_num = request.get_json().get("phone_num", "")
    if not validators.email(email):
        return jsonify({
            "error": "Email is invalid."
        }), HTTP_400_BAD_REQUEST

    customer.name = name
    customer.email = email
    customer.phone_num = phone_num

    db.session.commit()

    return jsonify({
        "id": customer.id,
        "name": customer.name
    }), HTTP_201_CREATED

@customers.delete("/<int:id>")
@jwt_required()
def delete_customer(id):
    customer = Customer.query.filter_by(id=id).first()
    if not Customer:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(customer)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
