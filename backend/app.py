from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os

app = Flask(__name__)
# 简化 CORS 配置，使用最宽松的设置
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization", "Accept"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# 配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'dev')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///lottery.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
jwt = JWTManager(app)

# 注册蓝图
from routes.lottery import lottery_bp
from routes.analysis import analysis_bp
from routes.prediction import prediction_bp
from routes.discussion import discussion_bp
from routes.auth import auth_bp

app.register_blueprint(lottery_bp, url_prefix='/api/lottery')
app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
app.register_blueprint(prediction_bp, url_prefix='/api/prediction')
app.register_blueprint(discussion_bp, url_prefix='/api/discussion')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 