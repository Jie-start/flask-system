from app import create_app, db
from app.models import Department, Position

app = create_app()

def init_data():
    # 添加初始部门
    departments = [
        '技术部',
        '人力资源部',
        '财务部',
        '市场部',
        '销售部'
    ]
    
    # 添加初始职位
    positions = [
        '工程师',
        '主管',
        '经理',
        '总监',
        '助理',
        '专员'
    ]
    
    with app.app_context():
        db.create_all()
        
        # 检查并添加部门
        for dept_name in departments:
            if not Department.query.filter_by(name=dept_name).first():
                dept = Department(name=dept_name)
                db.session.add(dept)
        
        # 检查并添加职位
        for pos_name in positions:
            if not Position.query.filter_by(title=pos_name).first():
                pos = Position(title=pos_name)
                db.session.add(pos)
        
        db.session.commit()

if __name__ == '__main__':
    init_data()  # 初始化基础数据
    app.run(debug=True) 