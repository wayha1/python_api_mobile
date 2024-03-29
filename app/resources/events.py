from flask_restx import Resource, Namespace, abort
from flask_jwt_extended import jwt_required
from app.resources.api_models import *
from app.models import *
from app.extensions import db
from app.authorize import authorizations

ns_events = Namespace('events' , authorizations=authorizations)

ns_events.decorators = [jwt_required()]

@ns_events.route('/cart')
class EventListAPI(Resource):
    @ns_events.doc(security= "jsonWebToken")
    @ns_events.marshal_list_with(cart_model)
    @jwt_required()
    def get(self):
        payments = Cart.query.all()
        return payments, 200
    
    @ns_events.doc(security= "jsonWebTOken")
    @ns_events.expect(cart_model_input)
    @ns_events.marshal_with(cart_model)
    def post(self):
        addCart = ns_events.payload
        
        # Check if 'user_id' is present in the payload
        if 'user_id' not in addCart:
            return {'message': 'Missing user_id in request payload'}, 400
        
        # Extract 'user_id', 'book_id', and 'quantity' from the payload
        user_id = addCart.get('user_id')
        book_id = addCart.get('book_id')
        quantity = addCart.get('quantity')
        
        # Check if any of the required fields are missing
        if user_id is None or book_id is None or quantity is None:
            return {'message': 'Missing required fields in request payload'}, 400
        
        # Create and add the cart item to the database
        cart = Cart(
            user_id=user_id,
            book_id=book_id,
            quantity=quantity
        )
        db.session.add(cart)
        db.session.commit()
        
        return cart, 201

@ns_events.route('/cart/<int:id>')
class EventAPI(Resource):
    @ns_events.doc(security="jsonWebToken")
    @ns_events.marshal_with(cart_model)
    def get(self, id):
        cart = Cart.query.get(id)
        if not cart:
            abort(404, message="Cart item not found")
        return cart, 200
    
    @ns_events.doc(security="jsonWebToken")
    @ns_events.expect(cart_model_input)
    @ns_events.marshal_with(cart_model)
    def put(self, id):
        cart_data = ns_events.payload
        cart = Cart.query.get(id)
        if not cart:
            abort(404, message="Cart item not found")
        cart.user_id = cart_data.get("user_id", cart.user_id)
        cart.book_id = cart_data.get("book_id", cart.book_id)
        cart.quantity = cart_data.get("quantity", cart.quantity)
        db.session.commit()
        return cart, 200

    @ns_events.doc(security="jsonWebToken")
    def delete(self, id):
        cart = Cart.query.get(id)
        if not cart:
            abort(404, message="Cart item not found")
        db.session.delete(cart)
        db.session.commit()
        return {}, 204  
    
@ns_events.route('/payment')
class PaymentAPI(Resource):
    @ns_events.doc(security="jsonWebToken")
    @ns_events.marshal_with(payment_model)
    def get(self):
        payments = Payment.query.all()
        return payments

    @ns_events.doc(security="jsonWebToken")
    @ns_events.expect(payment_input_model)
    @ns_events.marshal_with(payment_model)
    def post(self):
        payment_data = ns_events.payload
        payment = Payment(
            user_id=payment_data["user_id"],
            book_id=payment_data["book_id"],
            price=payment_data["price"],
            card_number=payment_data["card_number"],
            card_holder_name=payment_data["card_holder_name"],
            expiration_date=payment_data["expiration_date"],
            cvv=payment_data["cvv"]
        )
        db.session.add(payment)
        db.session.commit()
        return payment, 201


@ns_events.route('/payment/<int:id>')
class PaymentDetailAPI(Resource):
    @ns_events.doc(security="jsonWebToken")
    @ns_events.marshal_with(payment_model)
    def get(self, id):
        payment = Payment.query.get(id)
        if not payment:
            abort(404, message="Payment not found")
        return payment

    @ns_events.doc(security="jsonWebToken")
    @ns_events.expect(payment_input_model)
    @ns_events.marshal_with(payment_model)
    def put(self, id):
        payment_data = ns_events.payload
        payment = Payment.query.get(id)
        if not payment:
            abort(404, message="Payment not found")
        payment.user_id = payment_data.get("user_id", payment.user_id)
        payment.book_id = payment_data.get("book_id", payment.book_id)
        payment.price = payment_data.get("price", payment.price)
        payment.card_number = payment_data.get("card_number", payment.card_number)
        payment.card_holder_name = payment_data.get("card_holder_name", payment.card_holder_name)
        payment.expiration_date = payment_data.get("expiration_date", payment.expiration_date)
        payment.cvv = payment_data.get("cvv", payment.cvv)
        db.session.commit()
        return payment

    @ns_events.doc(security="jsonWebToken")
    def delete(self, id):
        payment = Payment.query.get(id)
        if not payment:
            abort(404, message="Payment not found")
        db.session.delete(payment)
        db.session.commit()
        return {}, 204