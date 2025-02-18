from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transaction.db'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

class DeliverySchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_date = db.Column(db.DateTime, nullable=False)
    delivery_address = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=db.func.now())
    due_date = db.Column(db.DateTime, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    payment_date = db.Column(db.DateTime, default=db.func.now())
    payment_amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)

class PaymentReconciliation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    reconciliation_date = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(50), nullable=False)

class ItemOfSale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    item_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class DeliveryConfirmation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(db.Integer, db.ForeignKey('delivery_schedule.id'), nullable=False)
    confirmation_date = db.Column(db.DateTime, default=db.func.now())
    confirmation_status = db.Column(db.String(50), nullable=False)

class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, nullable=False)
    referee_id = db.Column(db.Integer, nullable=False)
    referral_date = db.Column(db.DateTime, default=db.func.now())

class ReferralAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referral_id = db.Column(db.Integer, db.ForeignKey('referral.id'), nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    action_date = db.Column(db.DateTime, default=db.func.now())

class ReferralRedemption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referral_id = db.Column(db.Integer, db.ForeignKey('referral.id'), nullable=False)
    redemption_date = db.Column(db.DateTime, default=db.func.now())
    redemption_status = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
