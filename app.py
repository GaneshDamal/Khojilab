from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PER_PAGE'] = 10
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(1000), nullable=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prod_id = request.form['prod_id']
        prod_name = request.form['prod_name']
        prod_desc = request.form['prod_desc']
        prod_category = request.form['prod_category']
        prod_price = float(request.form['prod_price'])
        discount_percent = float(request.form['discount_percent']) if request.form['discount_percent'] else None
        prod_image = request.form['prod_image']
        
        
        # Create a new Product object and add it to the database
        new_product = Product(id=prod_id, name=prod_name, description=prod_desc, category=prod_category, 
                              price=prod_price, discount=float(discount_percent), image=prod_image)
        with app.app_context():
            db.session.add(new_product)
            db.session.commit()
        
        return redirect(url_for('display', prod_id=prod_id))
    else:
        return render_template('index.html')

@app.route('/display/<int:prod_id>')
def display(prod_id):
    with app.app_context():
        product = Product.query.get(prod_id)
        if product is None:
            return redirect(url_for('products'))
    return render_template('display.html', product=product)

@app.route('/product/')
@app.route('/product/<int:page>')
def products(page=1):
    with app.app_context():
        products = Product.query.order_by(desc(Product.id)).paginate(page, app.config['PER_PAGE'], error_out=False)
    return render_template('product.html', products=products)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
