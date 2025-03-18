from flask import Blueprint, jsonify, request
import random

bp = Blueprint('lottery', __name__)

@bp.route('/api/random/ssq', methods=['POST'])
def random_ssq():
    """双色球随机选号"""
    data = request.get_json()
    count = data.get('count', 1)  # 默认生成1注
    is_complex = data.get('is_complex', False)  # 是否复式
    
    results = []
    for _ in range(count):
        # 红球：1-33选6个
        red_balls = sorted(random.sample(range(1, 34), 6))
        # 蓝球：1-16选1个
        blue_ball = random.randint(1, 16)
        
        if is_complex:
            # 复式选号逻辑
            red_balls = [sorted(random.sample(range(1, 34), 7)) for _ in range(2)]
            blue_balls = [random.randint(1, 16) for _ in range(2)]
            results.append({
                'red_balls': red_balls,
                'blue_balls': blue_balls,
                'type': 'complex'
            })
        else:
            results.append({
                'red_balls': red_balls,
                'blue_ball': blue_ball,
                'type': 'simple'
            })
    
    return jsonify({'success': True, 'data': results})

@bp.route('/api/random/dlt', methods=['POST'])
def random_dlt():
    """大乐透随机选号"""
    data = request.get_json()
    count = data.get('count', 1)
    is_complex = data.get('is_complex', False)
    
    results = []
    for _ in range(count):
        # 前区：1-35选5个
        front_balls = sorted(random.sample(range(1, 36), 5))
        # 后区：1-12选2个
        back_balls = sorted(random.sample(range(1, 13), 2))
        
        if is_complex:
            # 复式选号逻辑
            front_balls = [sorted(random.sample(range(1, 36), 6)) for _ in range(2)]
            back_balls = [sorted(random.sample(range(1, 13), 3)) for _ in range(2)]
            results.append({
                'front_balls': front_balls,
                'back_balls': back_balls,
                'type': 'complex'
            })
        else:
            results.append({
                'front_balls': front_balls,
                'back_balls': back_balls,
                'type': 'simple'
            })
    
    return jsonify({'success': True, 'data': results}) 