from flask import Blueprint, jsonify, request
import random
import logging

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

lottery_bp = Blueprint('lottery', __name__)

@lottery_bp.route('/test', methods=['GET'])
def test_route():
    """测试路由"""
    logger.debug('收到测试请求')
    return jsonify({'message': '测试成功', 'status': 'ok'})

@lottery_bp.route('/types', methods=['GET'])
def get_lottery_types():
    """获取彩票类型列表"""
    types = [
        {'id': 'ssq', 'name': '双色球', 'description': '6个红球+1个蓝球'},
        {'id': 'dlt', 'name': '大乐透', 'description': '5个前区号码+2个后区号码'}
    ]
    return jsonify(types)

@lottery_bp.route('/random', methods=['POST'])
def generate_random_numbers():
    """生成随机号码"""
    try:
        logger.debug('收到随机选号请求')
        data = request.get_json()
        logger.debug(f'请求数据: {data}')
        
        lottery_type = data.get('type', 'ssq')
        count = data.get('count', 1)  # 获取选号数量
        
        if lottery_type == 'ssq':
            numbers = []
            for _ in range(count):
                red_balls = sorted(random.sample(range(1, 34), 6))
                blue_ball = random.randint(1, 16)
                numbers.append({
                    'red_balls': red_balls,
                    'blue_ball': blue_ball
                })
            logger.debug(f'生成的双色球号码: {numbers}')
            return jsonify({'numbers': numbers})
        elif lottery_type == 'dlt':
            numbers = []
            for _ in range(count):
                front_numbers = sorted(random.sample(range(1, 36), 5))
                back_numbers = sorted(random.sample(range(1, 13), 2))
                numbers.append({
                    'front_numbers': front_numbers,
                    'back_numbers': back_numbers
                })
            logger.debug(f'生成的大乐透号码: {numbers}')
            return jsonify({'numbers': numbers})
        else:
            logger.error(f'不支持的彩票类型: {lottery_type}')
            return jsonify({'error': '不支持的彩票类型'}), 400
    except Exception as e:
        logger.error(f'生成随机号码时发生错误: {str(e)}')
        return jsonify({'error': str(e)}), 500

@lottery_bp.route('/smart', methods=['POST'])
def generate_smart_numbers():
    """智能选号"""
    try:
        logger.debug('收到智能选号请求')
        data = request.get_json()
        logger.debug(f'请求数据: {data}')
        
        lottery_type = data.get('type', 'ssq')
        count = data.get('count', 1)  # 获取选号数量
        
        if lottery_type == 'ssq':
            numbers = []
            for _ in range(count):
                red_balls = sorted(random.sample(range(1, 34), 6))
                blue_ball = random.randint(1, 16)
                numbers.append({
                    'red_balls': red_balls,
                    'blue_ball': blue_ball,
                    'confidence': random.randint(60, 95),  # 模拟置信度
                    'explanation': '基于历史数据分析，选择了较为均衡的号码组合。'
                })
            logger.debug(f'生成的智能双色球号码: {numbers}')
            return jsonify({'numbers': numbers})
        elif lottery_type == 'dlt':
            numbers = []
            for _ in range(count):
                front_numbers = sorted(random.sample(range(1, 36), 5))
                back_numbers = sorted(random.sample(range(1, 13), 2))
                numbers.append({
                    'front_numbers': front_numbers,
                    'back_numbers': back_numbers,
                    'confidence': random.randint(60, 95),  # 模拟置信度
                    'explanation': '根据近期开奖趋势，选择了热温冷号码搭配的组合。'
                })
            logger.debug(f'生成的智能大乐透号码: {numbers}')
            return jsonify({'numbers': numbers})
        else:
            logger.error(f'不支持的彩票类型: {lottery_type}')
            return jsonify({'error': '不支持的彩票类型'}), 400
    except Exception as e:
        logger.error(f'生成智能号码时发生错误: {str(e)}')
        return jsonify({'error': str(e)}), 500

@lottery_bp.route('/history', methods=['GET'])
def get_history_data():
    """获取历史数据"""
    # TODO: 实现历史数据查询
    return jsonify({
        'message': '历史数据功能开发中'
    }) 