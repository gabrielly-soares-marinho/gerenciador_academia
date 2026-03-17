from flask import Blueprint, jsonify, request
from . import db
from .models import Member

bp = Blueprint('api', __name__)


@bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


@bp.route('/members', methods=['GET', 'POST'])
def members():
    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name')
        if not name:
            return jsonify({"error": "name required"}), 400
        m = Member(name=name, email=data.get('email'), phone=data.get('phone'))
        db.session.add(m)
        db.session.commit()
        return jsonify({"id": m.id, "name": m.name}), 201
    else:
        members = Member.query.all()
        return jsonify([{"id": m.id, "name": m.name, "email": m.email} for m in members])


@bp.route('/members/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def member_detail(id):
    m = Member.query.get_or_404(id)
    if request.method == 'GET':
        return jsonify({"id": m.id, "name": m.name, "email": m.email, "phone": m.phone})
    if request.method == 'PUT':
        data = request.get_json() or {}
        m.name = data.get('name', m.name)
        m.email = data.get('email', m.email)
        m.phone = data.get('phone', m.phone)
        db.session.commit()
        return jsonify({"id": m.id})
    if request.method == 'DELETE':
        db.session.delete(m)
        db.session.commit()
        return jsonify({"deleted": True})
