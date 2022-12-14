from flask import Blueprint, request
from init import db
from models.card import Card, CardSchema
from datetime import date
from flask_jwt_extended import jwt_required
from controllers.auth_controller import authorize

cards_bp = Blueprint('cards', __name__, url_prefix='/cards')

@cards_bp.route('/')
def get_all_cards():
    stmt = db.select(Card).order_by(Card.date.desc())
    cards = db.session.scalars(stmt)
    return CardSchema(many=True).dump(cards)
   

@cards_bp.route('/<int:id>/')
def get_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        return CardSchema().dump(card)
    else:
        return {'error': f'card not found with id {id}'}, 404


@cards_bp.route('/<int:id>/', methods=['DELETE'])
@jwt_required()
def delete_one_card(id):
    authorize()
    
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        db.session.delete(card)
        db.session.commit()
        return {'message': f"card '{card.title}' deleted successfully"}, 200
    else:
        return {'error': f'card not found with id {id}'}, 404
        

@cards_bp.route('/<int:id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_card(id):
    stmt = db.select(Card).filter_by(id=id)
    card = db.session.scalar(stmt)
    if card:
        # none returned with .get
        card.title = request.json.get('title') or card.title
        card.description = request.json.get('description') or card.description
        card.status = request.json.get('status') or card.status
        card.priority = request.json.get('priority') or card.priority
        db.session.commit()
        return CardSchema().dump(card)
    else:
        return {'error': f'card not found with id {id}'}, 404

@cards_bp.route('/', methods=['POST'])
@jwt_required()
def create_card():
        # Create a new Card model instance 
        card = Card(
            title = request.json['title'],
            description = request.json['description'],
            date = date.today(),
            status = request.json['status'],
            priority = request.json['priority']
        )
        # Add and commit card to DB
        db.session.add(card)
        db.session.commit()
        # respond to client
        return CardSchema().dump(card), 201
        
    
    