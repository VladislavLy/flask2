from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
import csv
from flask import Flask, request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datasales.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Transaction_date = db.Column(db.Integer, nullable=False)
    Product = db.Column(db.String(120), nullable=False)
    Price = db.Column(db.Integer,  nullable=False)
    Payment_Type = db.Column(db.String(120), nullable=False)


    def __repr__(self):
        return f'<Id {self.id} Transaction_date {self.Transaction_date}, Product {self.Product}, Price {self.Price}, Payment_Type {self.Payment_Type}>'


@app.route("/create")
def index():
    with open("templates/homework3sales.csv", encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter = ";")
        allofthem = []
        count =0
        for row in file_reader:
            user = User(Transaction_date=row["Transaction_date"], Product=row["Product"], Price=row["Price"], Payment_Type=row["Payment_Type"])
            db.session.add(user)
            db.session.commit()
            count +=1
    print(count)
    return "<p>FINE</p>"


@app.route("/summary/")
def getme():
    my_dict = {}
    for i in User.query.all():
        date = i.Transaction_date.split(" ")[0]
        if date not in my_dict.keys():
            my_dict.update({date: i.Price})
        else:
            my_dict[date] = int(i.Price) + int(my_dict.get(date))


    return render_template("main.html", dictionary= my_dict)


@app.route("/sales")
def get_specific():
    product = request.args.get('product')
    payment_type = request.args.get("payment_type")
    
    if product is not None and payment_type is not None:
        result = User.query.filter_by(Product=product.title(), Payment_Type=payment_type.title()).all()
    elif product is not None or payment_type is not None:
        if product is None:
            result = User.query.filter_by(Payment_Type=payment_type.title()).all()
        elif payment_type is None:
            result = User.query.filter_by(Product=product.title()).all()
    else:
        result = User.query.all()

    return render_template("specific.html", list = result)


@app.route("/")
def base():
    return render_template("base.html")


if __name__ == "__main__":
    app.run(debug=True)



