from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Department, Position, Employee, SalaryRecord, AttendanceRecord
from app import db
from datetime import datetime

bp = Blueprint('main', __name__)

# 首页
@bp.route('/')
def index():
    return render_template('index.html')

# 员工相关路由
@bp.route('/employees')
def list_employees():
    employees = Employee.query.all()
    return render_template('employees/list.html', employees=employees)

@bp.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee = Employee(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d'),
            department_id=request.form['department_id'],
            position_id=request.form['position_id']
        )
        db.session.add(employee)
        db.session.commit()
        flash('员工添加成功！')
        return redirect(url_for('main.list_employees'))
    departments = Department.query.all()
    positions = Position.query.all()
    return render_template('employees/add.html', departments=departments, positions=positions)

@bp.route('/employees/<int:id>/edit', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    departments = Department.query.all()
    positions = Position.query.all()
    
    if request.method == 'POST':
        employee.name = request.form.get('name')
        employee.gender = request.form.get('gender')
        employee.phone = request.form.get('phone')
        employee.email = request.form.get('email')
        employee.department_id = request.form.get('department_id')
        employee.position_id = request.form.get('position_id')
        employee.update_time = datetime.now()
        
        try:
            db.session.commit()
            flash('员工信息更新成功！', 'success')
            return redirect(url_for('main.list_employees'))
        except Exception as e:
            db.session.rollback()
            flash('更新失败，请重试！', 'danger')
            
    return render_template('employees/edit.html', 
                         employee=employee, 
                         departments=departments, 
                         positions=positions)

@bp.route('/employees/<int:id>/delete')
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    try:
        # 先删除关联的考勤记录
        AttendanceRecord.query.filter_by(employee_id=id).delete()
        
        # 删除关联的薪资记录
        SalaryRecord.query.filter_by(employee_id=id).delete()
        
        # 最后删除员工记录
        db.session.delete(employee)
        db.session.commit()
        flash('员工删除成功！', 'success')
    except Exception as e:
        db.session.rollback()
        flash('删除失败，请重试！', 'danger')
        
    return redirect(url_for('main.list_employees'))

# 部门管理路由
@bp.route('/departments')
def list_departments():
    departments = Department.query.all()
    return render_template('departments/list.html', departments=departments)

@bp.route('/departments/add', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        department = Department(name=request.form['name'])
        db.session.add(department)
        db.session.commit()
        flash('部门添加成功！')
        return redirect(url_for('main.list_departments'))
    return render_template('departments/add.html')

@bp.route('/departments/<int:id>/edit', methods=['GET', 'POST'])
def edit_department(id):
    department = Department.query.get_or_404(id)
    if request.method == 'POST':
        department.name = request.form['name']
        db.session.commit()
        flash('部门更新成功！')
        return redirect(url_for('main.list_departments'))
    return render_template('departments/edit.html', department=department)

# 工资管理路由
@bp.route('/salaries')
def list_salaries():
    salary_records = SalaryRecord.query.all()
    return render_template('salaries/list.html', salary_records=salary_records)

@bp.route('/salaries/add', methods=['GET', 'POST'])
def add_salary():
    if request.method == 'POST':
        salary = SalaryRecord(
            employee_id=request.form['employee_id'],
            amount=float(request.form['amount']),
            date=datetime.strptime(request.form['date'], '%Y-%m-%d')
        )
        db.session.add(salary)
        db.session.commit()
        flash('薪资记录添加成功！')
        return redirect(url_for('main.list_salaries'))
    employees = Employee.query.all()
    return render_template('salaries/add.html', employees=employees)

# 考勤管理路由
@bp.route('/attendance')
def list_attendance():
    attendance_records = AttendanceRecord.query.all()
    return render_template('attendance/list.html', attendance_records=attendance_records)

@bp.route('/attendance/add', methods=['GET', 'POST'])
def add_attendance():
    if request.method == 'POST':
        attendance = AttendanceRecord(
            employee_id=request.form['employee_id'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d'),
            status=request.form['status']
        )
        db.session.add(attendance)
        db.session.commit()
        flash('考勤记录添加成功！')
        return redirect(url_for('main.list_attendance'))
    employees = Employee.query.all()
    return render_template('attendance/add.html', employees=employees)

# 职位管理路��
@bp.route('/positions')
def list_positions():
    positions = Position.query.all()
    return render_template('positions/list.html', positions=positions)

@bp.route('/positions/add', methods=['GET', 'POST'])
def add_position():
    if request.method == 'POST':
        position = Position(title=request.form['title'])
        db.session.add(position)
        db.session.commit()
        flash('职位添加成功！')
        return redirect(url_for('main.list_positions'))
    return render_template('positions/add.html')

@bp.route('/positions/<int:id>/edit', methods=['GET', 'POST'])
def edit_position(id):
    position = Position.query.get_or_404(id)
    if request.method == 'POST':
        position.title = request.form['title']
        db.session.commit()
        flash('职位更新成功！')
        return redirect(url_for('main.list_positions'))
    return render_template('positions/edit.html', position=position)

@bp.route('/positions/<int:id>/delete')
def delete_position(id):
    position = Position.query.get_or_404(id)
    db.session.delete(position)
    db.session.commit()
    flash('职位删除成功！')
    return redirect(url_for('main.list_positions')) 