# app.py

from flask import Flask
from config import Config
from models import db, User
from auth import login_bp, login_manager
from routes.prisoner import prisoner_bp
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config.from_object(Config)

# 初始化扩展
db.init_app(app)
login_manager.init_app(app)

# 注册蓝图
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(prisoner_bp)


def initialize_database():
    """
    在 app 上下文里手动创建表，如果不存在就创建，并插入示例狱警账号。
    """
    with app.app_context():
        db.create_all()
        # 检查演示账号是否已存在
        if not User.query.filter_by(username='officer1').first():
            demo = User(
                username='officer1',
                password=generate_password_hash('123456'),
                role='officer'
            )
            db.session.add(demo)
            db.session.commit()
        print("数据库初始化完成 √")


if __name__ == '__main__':
    # 启动前先初始化数据库
    initialize_database()

    port = int(os.environ.get('PORT', 3000))
    # debug=True 仅在本地开发时用，生产环境请改为 False
    app.run(host='0.0.0.0', port=port, debug=True)
