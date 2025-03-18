from app import db
from datetime import datetime

class LotteryHistory(db.Model):
    """历史开奖记录"""
    id = db.Column(db.Integer, primary_key=True)
    lottery_type = db.Column(db.String(10), nullable=False)  # ssq/dlt
    period = db.Column(db.String(20), nullable=False)  # 期号
    draw_date = db.Column(db.Date, nullable=False)  # 开奖日期
    numbers = db.Column(db.String(100), nullable=False)  # 开奖号码
    prize_pool = db.Column(db.Float)  # 奖池金额
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserPreference(db.Model):
    """用户选号偏好"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lottery_type = db.Column(db.String(10), nullable=False)
    favorite_numbers = db.Column(db.String(100))  # 常用号码
    exclude_numbers = db.Column(db.String(100))  # 排除号码
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PredictionRecord(db.Model):
    """预测记录"""
    id = db.Column(db.Integer, primary_key=True)
    lottery_type = db.Column(db.String(10), nullable=False)
    period = db.Column(db.String(20), nullable=False)
    predicted_numbers = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float)  # 预测置信度
    actual_numbers = db.Column(db.String(100))  # 实际开奖号码
    is_correct = db.Column(db.Boolean)  # 是否预测正确
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    """用户信息"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    preferences = db.relationship('UserPreference', backref='user', lazy=True) 