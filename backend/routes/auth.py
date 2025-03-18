from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # TODO: 实现用户验证
    if username == 'test' and password == 'test':
        access_token = create_access_token(identity=1)
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': 1,
                'username': username,
                'email': 'test@example.com'
            }
        })
    else:
        return jsonify({'error': '用户名或密码错误'}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    # TODO: 实现用户注册
    return jsonify({
        'message': '注册成功'
    })

@auth_bp.route('/user/info', methods=['GET'])
@jwt_required()
def get_user_info():
    """获取用户信息"""
    user_id = get_jwt_identity()
    
    # TODO: 实现用户信息查询
    return jsonify({
        'id': user_id,
        'username': 'test',
        'email': 'test@example.com'
    })

@auth_bp.route('/user/info', methods=['PUT'])
@jwt_required()
def update_user_info():
    """更新用户信息"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # TODO: 实现用户信息更新
    return jsonify({
        'message': '更新成功'
    }) 