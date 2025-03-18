from flask import Blueprint, jsonify, request
import random
from datetime import datetime, timedelta
import numpy as np

analysis_bp = Blueprint('analysis', __name__)

def generate_dates(periods):
    """生成日期列表"""
    end_date = datetime.now()
    dates = []
    for i in range(periods):
        dates.append((end_date - timedelta(days=i*2)).strftime('%Y-%m-%d'))
    return list(reversed(dates))

def generate_ssq_data(periods):
    """生成双色球数据"""
    dates = generate_dates(periods)
    red_balls = [random.randint(1, 33) for _ in range(periods)]
    blue_balls = [random.randint(1, 16) for _ in range(periods)]
    
    # 生成更有意义的K线数据
    values = []
    for i in range(periods):
        # 随机生成4个红球作为开高低收
        nums = sorted(random.sample(range(1, 34), 4))
        values.append({
            'open': nums[0],    # 开盘值（最小）
            'close': nums[3],   # 收盘值（最大）
            'low': nums[1],     # 最低值
            'high': nums[2],    # 最高值
            'volume': random.randint(100, 1000)  # 成交量
        })
    
    return dates, red_balls, blue_balls, values

def generate_dlt_data(periods):
    """生成大乐透数据"""
    dates = generate_dates(periods)
    front_numbers = [random.randint(1, 35) for _ in range(periods)]
    back_numbers = [random.randint(1, 12) for _ in range(periods)]
    
    # 生成更有意义的K线数据
    values = []
    for i in range(periods):
        # 随机生成4个前区号码作为开高低收
        nums = sorted(random.sample(range(1, 36), 4))
        values.append({
            'open': nums[0],    # 开盘值（最小）
            'close': nums[3],   # 收盘值（最大）
            'low': nums[1],     # 最低值
            'high': nums[2],    # 最高值
            'volume': random.randint(100, 1000)  # 成交量
        })
    
    return dates, front_numbers, back_numbers, values

@analysis_bp.route('/trend', methods=['GET'])
def get_trend_data():
    """获取趋势数据"""
    lottery_type = request.args.get('type', 'ssq')
    periods = int(request.args.get('periods', '30'))
    
    if lottery_type == 'ssq':
        dates, red_balls, blue_balls, _ = generate_ssq_data(periods)
        return jsonify({
            'data': {
                'dates': dates,
                'red_balls': red_balls,
                'blue_balls': blue_balls
            }
        })
    else:  # dlt
        dates, front_numbers, back_numbers, _ = generate_dlt_data(periods)
        return jsonify({
            'data': {
                'dates': dates,
                'front_numbers': front_numbers,
                'back_numbers': back_numbers
            }
        })

@analysis_bp.route('/kline', methods=['GET'])
def get_kline_data():
    """获取K线数据"""
    lottery_type = request.args.get('type', 'ssq')
    periods = int(request.args.get('periods', '30'))
    
    if lottery_type == 'ssq':
        dates, _, _, values = generate_ssq_data(periods)
    else:  # dlt
        dates, _, _, values = generate_dlt_data(periods)
    
    return jsonify({
        'data': {
            'dates': dates,
            'values': values
        }
    })

@analysis_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据"""
    lottery_type = request.args.get('type', 'ssq')
    
    if lottery_type == 'ssq':
        return jsonify({
            'data': {
                'red_ball_stats': {
                    'hot_numbers': [random.randint(1, 33) for _ in range(3)],
                    'cold_numbers': [random.randint(1, 33) for _ in range(3)],
                    'frequency': {
                        '1-10': random.randint(20, 40),
                        '11-20': random.randint(30, 50),
                        '21-33': random.randint(20, 40)
                    }
                },
                'blue_ball_stats': {
                    'hot_numbers': [random.randint(1, 16) for _ in range(3)],
                    'cold_numbers': [random.randint(1, 16) for _ in range(3)],
                    'frequency': {
                        '1-5': random.randint(20, 40),
                        '6-10': random.randint(30, 50),
                        '11-16': random.randint(20, 40)
                    }
                }
            }
        })
    else:  # dlt
        return jsonify({
            'data': {
                'front_numbers_stats': {
                    'hot_numbers': [random.randint(1, 35) for _ in range(3)],
                    'cold_numbers': [random.randint(1, 35) for _ in range(3)],
                    'frequency': {
                        '1-12': random.randint(20, 40),
                        '13-24': random.randint(30, 50),
                        '25-35': random.randint(20, 40)
                    }
                },
                'back_numbers_stats': {
                    'hot_numbers': [random.randint(1, 12) for _ in range(3)],
                    'cold_numbers': [random.randint(1, 12) for _ in range(3)],
                    'frequency': {
                        '1-4': random.randint(20, 40),
                        '5-8': random.randint(30, 50),
                        '9-12': random.randint(20, 40)
                    }
                }
            }
        })

@analysis_bp.route('/predict', methods=['GET'])
def predict_numbers():
    """预测号码"""
    lottery_type = request.args.get('type', 'ssq')
    periods = int(request.args.get('periods', '30'))
    
    if lottery_type == 'ssq':
        dates, red_balls, blue_balls, _ = generate_ssq_data(periods)
        
        # 使用简单的统计方法预测
        red_freq = {}
        for num in red_balls:
            red_freq[num] = red_freq.get(num, 0) + 1
            
        blue_freq = {}
        for num in blue_balls:
            blue_freq[num] = blue_freq.get(num, 0) + 1
            
        # 选择出现频率最高的号码
        predicted_red = sorted(red_freq.items(), key=lambda x: x[1], reverse=True)[:6]
        predicted_blue = sorted(blue_freq.items(), key=lambda x: x[1], reverse=True)[0]
        
        # 计算置信度
        confidence = min(max(sum([f for _, f in predicted_red]) / (periods * 6), 0.1), 0.9)
        
        return jsonify({
            'data': {
                'red_balls': [num for num, _ in predicted_red],
                'blue_ball': predicted_blue[0],
                'confidence': confidence,
                'explanation': '基于历史数据频率分析，选择出现次数最多的号码组合。'
            }
        })
    else:  # dlt
        dates, front_numbers, back_numbers, _ = generate_dlt_data(periods)
        
        # 使用简单的统计方法预测
        front_freq = {}
        for num in front_numbers:
            front_freq[num] = front_freq.get(num, 0) + 1
            
        back_freq = {}
        for num in back_numbers:
            back_freq[num] = back_freq.get(num, 0) + 1
            
        # 选择出现频率最高的号码
        predicted_front = sorted(front_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        predicted_back = sorted(back_freq.items(), key=lambda x: x[1], reverse=True)[:2]
        
        # 计算置信度
        confidence = min(max(sum([f for _, f in predicted_front]) / (periods * 5), 0.1), 0.9)
        
        return jsonify({
            'data': {
                'front_numbers': [num for num, _ in predicted_front],
                'back_numbers': [num for num, _ in predicted_back],
                'confidence': confidence,
                'explanation': '基于历史数据频率分析，选择出现次数最多的号码组合。'
            }
        })

@analysis_bp.route('/optimize', methods=['POST'])
def optimize_numbers():
    """优化号码"""
    data = request.get_json()
    lottery_type = data.get('lotteryType', 'ssq')
    selected_numbers = data.get('numbers', [])
    
    if not selected_numbers:
        return jsonify({
            'error': '请选择至少一个号码'
        }), 400
    
    # 根据彩票类型确定号码范围
    if lottery_type == 'ssq':
        # 双色球: 红球1-33，蓝球1-16
        red_range = list(range(1, 34))
        blue_range = list(range(1, 17))
        
        # 从用户选择的号码中筛选出红球
        user_red = [num for num in selected_numbers if 1 <= num <= 33]
        
        # 如果用户选择的红球不足6个，随机补充
        if len(user_red) < 6:
            remaining_red = [num for num in red_range if num not in user_red]
            additional_red = random.sample(remaining_red, 6 - len(user_red))
            optimized_red = sorted(user_red + additional_red)
        else:
            # 如果超过6个，选择其中的6个
            optimized_red = sorted(random.sample(user_red, 6))
        
        # 随机选择一个蓝球
        optimized_blue = random.choice(blue_range)
        
        return jsonify({
            'numbers': {
                'red': optimized_red,
                'blue': optimized_blue
            }
        })
    else:  # dlt
        # 大乐透: 前区1-35，后区1-12
        front_range = list(range(1, 36))
        back_range = list(range(1, 13))
        
        # 从用户选择的号码中筛选出前区号码
        user_front = [num for num in selected_numbers if 1 <= num <= 35]
        
        # 如果用户选择的前区号码不足5个，随机补充
        if len(user_front) < 5:
            remaining_front = [num for num in front_range if num not in user_front]
            additional_front = random.sample(remaining_front, 5 - len(user_front))
            optimized_front = sorted(user_front + additional_front)
        else:
            # 如果超过5个，选择其中的5个
            optimized_front = sorted(random.sample(user_front, 5))
        
        # 随机选择两个后区号码
        optimized_back = sorted(random.sample(back_range, 2))
        
        return jsonify({
            'numbers': {
                'front': optimized_front,
                'back': optimized_back
            }
        }) 