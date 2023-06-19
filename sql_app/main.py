from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db,User
from models import Student, StudentUpdate,StudentCreate,UserIn,SignIn
from fastapi.responses import JSONResponse
# from database import SessionLocal, engine

app = FastAPI()

#根目录
@app.get("/")
async def root():
    return JSONResponse(content={"message": "欢迎访问我的学生信息管理API!"})

#查询所有学生信息
@app.get("/students")
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = db.query(Student).offset(skip).limit(limit).all()
    return students

# 根据班级查询学生信息
@app.get("/students/{classname}")
def read_students_by_classname(classname: str, db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.classname == classname).all()
    if not students:
        raise HTTPException(status_code=404, detail="找不到班级名")
    return students


# 更新学生信息
@app.put("/students/{student_id}")
async def update_student(student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)):
    # 查询指定 ID 的学生记录
    student = db.query(Student).filter(Student.id == student_id).first()

    # 如果找不到对应的学生，则返回错误响应
    if not student:
        raise HTTPException(status_code=404, detail="找不到指定的学生")

    # 更新学生信息
    for field, value in student_update.dict(exclude_unset=True).items():
        setattr(student, field, value)
    db.commit()

    return {"msg": "学生信息已更新"}

# 删除学生信息
@app.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    # 查询指定 ID 的学生记录
    student = db.query(Student).filter(Student.id == student_id).first()

    # 如果找不到对应的学生，则返回错误响应
    if not student:
        raise HTTPException(status_code=404, detail="找不到指定的学生")

    # 删除学生记录
    db.delete(student)
    db.commit()

    return {"msg": "学生信息已删除"}

# 添加学生信息
@app.post("/students")
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # 创建学生记录
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return {"msg": "学生信息添加成功", "data": db_student}


# 查询某个学生信息的接口函数
@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="找不到指定的学生")
    return student



@app.post("/signin")
def signin(user:SignIn, db: Session = Depends(get_db)):
    # 检查用户名是否已经存在
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="该用户名已经被注册了")

    # 验证两次密码输入是否相同
    if user.password != user.once_password:
        raise HTTPException(status_code=400, detail="两次密码输入不一致，请确认后重新输入")
    
    if not user.username or not user.password or not user.once_password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")

    # 创建新用户对象
    user = User(username=user.username, password=user.password)

    # 将用户对象添加到数据库中并提交事务
    db.add(user)
    db.commit()

    # 返回创建的用户对象
    return {"msg": "恭喜你注册成功！", "data": user}


@app.post("/login")
def login(user: UserIn, db: Session = Depends(get_db)):
    # 检查用户名是否存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="该用户不存在")

    # 检查密码是否正确
    if existing_user.password != user.password:
        raise HTTPException(status_code=400, detail="密码错误")

    return {"msg": "登录成功", "data": existing_user}

