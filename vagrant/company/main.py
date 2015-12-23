from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Company, Employee

app = Flask(__name__)

engine = create_engine('postgres://sidnyhkwqbgjkt:CexV9BNqGXnscszhGJvK4oK9wj@ec2-107-22-184-127.compute-1.amazonaws.com:5432/dedc5jc5msbsv3')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def companyList():
    companies = session.query(Company).all()
    return render_template('index.html', companies = companies)

#Create a new company
@app.route('/company/new/', methods=['GET', 'POST'])
def newCompany():
    if request.method == 'POST':
        newCompany = Company(name = request.form['name'])
        session.add(newCompany)
        session.commit()
        return redirect(url_for('companyList'))
    if request.method == 'GET':
        return render_template('newcompany.html')

#Edit a company
@app.route('/company/<int:company_id>/edit', methods=['GET', 'POST'])
def editCompany(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    if request.method == 'POST':
        if company != []:
            company.name = request.form['name']
            session.add(company)
            session.commit()
            return redirect(url_for('companyList'))
    if request.method == 'GET':
        return render_template('editcompany.html', company = company)

#List all employees in a company
@app.route('/company/<int:company_id>/')
def employeeList(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    employees = session.query(Employee).filter_by(company_id=company_id)
    return render_template('list.html', company=company, employees = employees)

#Making an API Endpoint to get list of employees
@app.route('/company/<int:company_id>/list/JSON')
def employeeListJSON(company_id):
    company = session.query(Company).filter_by(id = company_id).one()
    employees = session.query(Employee).filter_by(company_id= 
        company_id).all()
    return jsonify(Employees=[i.serialize for i in employees])

#Making an API Endpoint to get one employee
@app.route('/company/<int:company_id>/list/<int:employee_id>/JSON')
def employeeJSON(company_id, employee_id):
    company = session.query(Company).filter_by(id = company_id).one()
    employee = session.query(Employee).filter_by(company_id= 
        company_id, id = employee_id).one()
    return jsonify(Employee=employee.serialize)

# Create new employee

@app.route('/company/<int:company_id>/newemployee', methods=[
    'GET', 'POST'])
def newEmployee(company_id):
    if request.method == 'POST':
        newemployee = Employee(firstname = request.form['firstname'], 
            lastname = request.form['lastname'], zipcode = 
            request.form['zipcode'], birthyear = request.form['birthyear'],
            birthmonth = request.form['birthmonth'], birthday = 
            request.form['birthday'], company_id = company_id)
        session.add(newemployee)
        session.commit()
        flash("New employee has been added!")
        return redirect(url_for('employeeList',company_id=company_id))
    if request.method == 'GET':
        return render_template('newemployee.html', company_id = 
            company_id)
    

# Edit employee

@app.route('/company/<int:company_id>/employee/<int:employee_id>/', 
    methods=['GET', 'POST'])
def editEmployee(company_id, employee_id, ):
    if request.method == 'POST':
        editEmployee = session.query(Employee).filter_by(id = employee_id, 
            company_id = company_id).one()
        if editEmployee != []:
            editEmployee.firstname = request.form['firstname']
            editEmployee.lastname = request.form['lastname']
            editEmployee.zipcode = request.form['zipcode']
            editEmployee.birthday = request.form['birthday']
            editEmployee.birthmonth = request.form['birthmonth']
            editEmployee.birthyear = request.form['birthyear']
            session.add(editEmployee)
            session.commit()
            flash("Your employee has been edited!")
        return redirect(url_for('employeeList', company_id = 
            company_id))
    elif request.method == 'GET':
        editEmployee = session.query(Employee).filter_by(id = employee_id,
            company_id = company_id).one()
        return render_template('editemployee.html', company_id =
            company_id, employee_id = employee_id, employee=editEmployee)

# Delete employee

@app.route('/company/<int:company_id>/delete/<int:employee_id>/',
    methods=['GET', 'POST'])
def deleteEmployee(company_id, employee_id):
    if request.method == 'POST':
        deleteEmployee = session.query(Employee).filter_by(id = employee_id,
            company_id = company_id).one()
        if deleteEmployee != []:
            session.delete(deleteEmployee)
            session.commit()
            flash("Your employee has been deleted!")
        return redirect(url_for('employeeList', company_id =
            company_id))
    if request.method == 'GET':
        employee = session.query(Employee).filter_by(id = employee_id,
            company_id = company_id).one()
        return render_template('deleteemployee.html', company_id =
            company_id, employee_id = employee_id, employee = employee)

#if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
 #   app.run(host='0.0.0.0', port=5000)