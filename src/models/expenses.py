import json
from flask import Blueprint, request, jsonify
import validators
from src.constants.http_status_codes import HTTP_204_NO_CONTENT,HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT, HTTP_201_CREATED, HTTP_200_OK
from src.database import Expense, db
from flask_jwt_extended import get_jwt_identity, jwt_required
expenses = Blueprint("expenses",__name__,url_prefix="/api/v1/expenses")

@expenses.route("/", methods=["POST", "GET"])
@jwt_required()
def handle_expenses():
    current_user = get_jwt_identity()
    if request.method == "POST":
        type = request.get_json().get("type", "")
        description = request.get_json().get("description", "")
        value = request.get_json().get("value", "")
        due_date = request.get_json().get("due_date", "")
        
        if Expense.query.filter_by(value=value, due_date=due_date).first():
            return jsonify({
                "error": "Expense already exists."
            }), HTTP_409_CONFLICT

        expense = Expense(
            type = type, 
            description = description,
            value = value,
            due_date = due_date
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "description": expense.description,
            "value": expense.value,
            "due_date": expense.due_date
        }), HTTP_201_CREATED
    
    else:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        expenses = Expense.query.paginate(page=page, per_page=per_page)
        
        data = []
        for expense in expenses.items:
            data.append({
                "description": expense.description,
                "value": expense.value,
                "due_date": expense.due_date
            })
        meta = {
            "page": expenses.page,
            "pages": expenses.pages,
            "total": expenses.total,
            "prev_page": expenses.prev_num,
            "next_page": expenses.next_num,
            "has_next": expenses.has_next,
            "has_prev": expenses.has_prev
        }
        return jsonify ({
            "data": data,
            "meta": meta
        }), HTTP_200_OK
        
@expenses.get("/<int:id>")
@jwt_required()
def get_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    if not expense:
        return jsonify({
            "message": "Item not found."
        })
    return jsonify({
        "description": expense.description,
        "value": expense.value,
        "due_date": expense.due_date
    }), HTTP_200_OK

@expenses.put("/<int:id>")
@expenses.patch("/<int:id>")
@jwt_required()
def edit_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    if not Expense:
        return jsonify({
            "message": "Item not found."
        })
    
    type = request.get_json().get("type", "")
    description = request.get_json().get("description", "")
    value = request.get_json().get("value", "")
    due_date = request.get_json().get("due_date", "")
    
    expense.type = type
    expense.type = description
    expense.type = value
    expense.type = due_date

    db.session.commit()

    return jsonify({
        "description": expense.description,
        "value": expense.value,
        "due_date": expense.due_date
    }), HTTP_201_CREATED

@expenses.delete("/<int:id>")
@jwt_required()
def delete_expense(id):
    expense = Expense.query.filter_by(id=id).first()
    if not expense:
        return jsonify({
            "message": "Item not found."
        })
    db.session.delete(expense)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT
