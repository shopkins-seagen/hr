from datetime import date, datetime

from flask import Flask, redirect, url_for, render_template, session, request, jsonify, flash, send_from_directory
from flask_wtf import FlaskForm
from wtforms.fields import DateField, IntegerField
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired
from wtforms import validators, SubmitField
from models import Employee, get_employees, add_employee, get_employee, delete_employee, update_employee, upload_employees,generate_report, review_employee, get_reviews
from werkzeug.utils import secure_filename
import os

SECRET_KEY = 'test'

app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
            static_folder='static')

app.config['SECRET_KEY'] = 'key'
app.config['UPLOADS'] = 'static/uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        value = int(request.form['edit'])
        return redirect(url_for('edit', id=value))

    employees = get_employees()

    page = request.args.get('page', 1, type=int)
    per_page = 12
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (employees.count() + per_page - 1) // per_page

    data = employees[start:end]
    return render_template('index.html', employees=data,pages=total_pages, page=page)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        emp = {'id': id,
              'name': request.form["name"],
              'address': request.form["address"],
              'ssn': request.form["ssn"],
              'dob':  request.form["dob"]  ,
              'title': request.form["title"],
              'started': request.form["started"],
              'ended': request.form["ended"]}


        response = update_employee(emp)
        if response[0]:
            flash(message='Employee Updated',category='success')

        return redirect(url_for('index'))
    return render_template('edit.html', id=id, reviews=get_reviews(id), employee=get_employee(id))


@app.route('/review/<int:id>', methods=['GET', 'POST'])
def review(id):
    employee=get_employee(id)
    if request.method == 'POST':
            review = {'employee_id': id,
                      'review_date': request.form["review_date"],
                      'rating': request.form["rating"],
                      'comment': request.form["comment"]}
            review_employee(review)
            return redirect(url_for('edit', id=id))
    return render_template('review.html', id=id, employee=employee)


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    delete_employee(id)
    return redirect(url_for('index'))
    # return render_template('index.html', employees=get_employees())


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        emp = {'name': request.form["name"],
               'address': request.form["address"],
               'ssn': request.form["ssn"],
               'dob': request.form["dob"],
               'title': request.form["title"],
               'started': request.form["started"]}
        response = add_employee(emp)
        print(f'response: {response}')
        if response[0]:
            flash(message='Employee Added', category='success')
        else:
            flash(message=response[1], category='fail')

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files['file']
        filename = secure_filename(file.filename)
        fn = os.path.join(app.config['UPLOADS'], filename)
        file.save(fn)
        upload_employees(fn)
        return redirect('/')
    return render_template('upload.html')


@app.route("/reports", methods=['GET', 'POST'])
def report():
    rpts = {
        1:"all_employees",
        2:"terminated_employees",
        3:"review_due"
    }
    if request.method == 'POST':
        report_type = request.values.get('options')
        report_name = rpts[int(request.values.get('options'))]
        fn = os.path.join(app.config['UPLOADS'], f"{report_name}.csv")
        generate_report(report_type, fn)
        flash(message=f"Report '{fn}' created in the downloads folder", category='success')
        return send_from_directory(os.path.join(app.config['UPLOADS']), f"{report_name}.csv")

    return render_template('reports.html')



if __name__ == '__main__':
    app.run(debug=True)
