from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 导入路由
from routes import lottery_routes, analysis_routes, prediction_routes
app.register_blueprint(lottery_routes.bp)
app.register_blueprint(analysis_routes.bp)
app.register_blueprint(prediction_routes.bp)

if __name__ == '__main__':
    app.run(debug=True) 