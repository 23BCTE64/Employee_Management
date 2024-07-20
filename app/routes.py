from flask import Blueprint, request, jsonify
from . import db
from .model import Employee
from .schemas import employee_schema, employees_schema
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app.errors import bad_request_error, not_found_error, handle_validation_error, \
    handle_sqlalchemy_error, handle_generic_error

routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
    """Returns a welcome message for the Employee Management System."""
    return "WELCOME TO THE EMPLOYEE MANAGEMENT SYSTEM"


# Create Employee
@routes.route('/employee', methods=['POST'])
def create_employee():
    """Creates a new employee record in the database."""
    if request.content_type != 'application/json':
        return bad_request_error("Content-Type must be application/json")

    try:
        data = request.get_json()
        new_emp = employee_schema.load(data)
        employee = Employee(name=new_emp['name'], dept=new_emp['dept'], position=new_emp['position'], salary=new_emp['salary'])

        db.session.add(employee)
        db.session.commit()
    except ValidationError as e:
        # Handle Marshmallow validation errors
        return handle_validation_error(e)
    except SQLAlchemyError as e:
        # Handle database errors
        return handle_sqlalchemy_error(e)

    return jsonify(employee_schema.dump(employee)), 201


# Read specific employee by ID
@routes.route('/employee/<int:employee_id>', methods=['GET'])
def get_emp(employee_id):
    """Retrieves and returns information for a specific employee."""
    employee = Employee.query.get(employee_id)
    if not employee:
        return not_found_error(f"Employee with id {employee_id} not found!")

    return jsonify(employee_schema.dump(employee)), 200


# Update details for existing employee
@routes.route('/employee/<int:employee_id>', methods=['PUT'])
def update_emp(employee_id):
    """Updates existing employee information."""
    if request.content_type != 'application/json':
        return bad_request_error("Content-Type must be application/json")

    employee = Employee.query.get(employee_id)
    if not employee:
        return not_found_error("Employee not found")

    try:
        data = request.get_json()
        updated_data = employee_schema.load(data, partial=True)

        if 'name' in updated_data:
            employee.name = updated_data['name']
        if 'dept' in updated_data:
            employee.dept = updated_data['dept']
        if 'position' in updated_data:
            employee.position = updated_data['position']
        if 'salary' in updated_data:
            employee.salary = updated_data['salary']

        db.session.commit()
    except ValidationError as e:
        # Handle Marshmallow validation errors during update
        return handle_validation_error(e)
    except SQLAlchemyError as e:
        # Handle database errors during update
        return handle_sqlalchemy_error(e)

    return jsonify({"message": "Employee updated successfully"}), 200


# Delete an employee
@routes.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_emp(employee_id):
    """Deletes an employee record from the database."""
    employee = Employee.query.get(employee_id)
    if not employee:
        return not_found_error("Employee not found")

    try:
        db.session.delete(employee)
        db.session.commit()
    except SQLAlchemyError as e:
        # Handle database errors during deletion
        return handle_sqlalchemy_error(e)

    return jsonify({"message": "Employee deleted successfully!"}), 200