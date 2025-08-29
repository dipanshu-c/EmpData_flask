from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"{self.id} - {self.name}"

# Home Page (Show form + employee list)
@app.route("/")
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

# Add Employee (form POST)
@app.route("/add_employee", methods=["POST"])
def add_employee():
    name = request.form["name"]
    email = request.form["email"]
    position = request.form["position"]
    # check if email already exists
    if not Employee.query.filter_by(email=email).first():
        new_employee = Employee(name=name, email=email, position=position)
        db.session.add(new_employee)
        db.session.commit()

    return redirect(url_for("index"))

# Delete Employee
@app.route("/delete/<int:id>")
def delete(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for("index"))

# Update Employee
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.email = request.form['email']
        employee.position = request.form['position']
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", employee=employee)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
