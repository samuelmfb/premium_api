import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import Income, db
from flask_jwt_extended import get_jwt_identity, jwt_required
incomes = Blueprint("incomes",__name__,url_prefix="/api/v1/incomes")

@incomes.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_incomes():
    current_user = get_jwt_identity()
    if request.method == "POST":

        customer = request.get_json().get("customer", "")
        project = request.get_json().get("project", "")
        value = request.get_json().get("value", "")
        date = request.get_json().get("date", "")

        if Income.query.filter_by(customer=customer, project=project, value=value, date=date).first():
            return jsonify({
                "error": "Income already exists."
            }), HTTP_409_CONFLICT

        income = Income(
            customer = request.get_json().get("customer", ""),
            project = request.get_json().get("project", ""),
            value = request.get_json().get("value", ""),
            date = request.get_json().get("date", "")
        )

        db.session.add(income)
        db.session.commit()

        return jsonify({
            "customer": income.customer,
            "project": income.project,
            "value": income.value,
            "date": income.date
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        incomes = Customer.query.paginate(page=page, per_page=per_page)
        
        data = []
        for Customer in incomes.items:
            data.append({
                "customer": income.customer,
                "project": income.project,
                "value": income.value,
                "date": income.date
            })
        meta = {
            "page": incomes.page,
            "pages": incomes.pages,
            "total": incomes.total,
            "prev_page": incomes.prev_num,
            "next_page": incomes.next_num,
            "has_next": incomes.has_next,
            "has_prev": incomes.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@incomes.get("/<int:id>")
@jwt_required()
def get_income(id):
    income = Income.query.filter_by(id=id).first()
    if not income:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "customer": income.customer,
        "project": income.project,
        "value": income.value,
        "date": income.date
    }), HTTP_200_OK

@incomes.put("/<int:id>")
@incomes.patch("/<int:id>")
@jwt_required()
def edit_income(id):
    income = Income.query.filter_by(id=id).first()
    if not income:
        return jsonify({
            "message": "Item not found."
        })
    
    customer = request.get_json().get("customer", "")
    project = request.get_json().get("project", "")
    value = request.get_json().get("value", "")
    date = request.get_json().get("date", "")

    income.customer = customer
    income.project = project
    income.value = value
    income.date = date

    db.session.commit()

    return jsonify({
        "customer": income.customer,
        "project": income.project,
        "value": income.value,
        "date": income.date
    }), HTTP_201_CREATED

@incomes.delete("/<int:id>")
@jwt_required()
def delete_Customer(id):
    Customer = Customer.query.filter_by(id=id).first()
    if not Customer:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(Customer)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
