/* eslint-disable */
/* eslint-disable prettier/prettier */
<template>
  <div class="prediction">
    <el-card class="prediction-card">
      <div slot="header">
        <h2>预测系统</h2>
      </div>

      <!-- 预测区域 -->
      <el-row :gutter="20" class="prediction-section">
        <el-col :span="16">
          <el-card class="prediction-result">
            <div slot="header">
              <h3>本期预测</h3>
            </div>
            <div class="prediction-content">
              <div class="lottery-type">
                <el-radio-group v-model="currentLottery">
                  <el-radio label="ssq">双色球</el-radio>
                  <el-radio label="dlt">大乐透</el-radio>
                </el-radio-group>
              </div>
              <div class="numbers-display">
                <template v-if="currentLottery === 'ssq'">
                  <div class="number-group">
                    <span
                      v-for="(num, index) in prediction.red_balls"
                      :key="'red' + index"
                      class="number red"
                    >
                      {{ num }}
                    </span>
                  </div>
                  <div class="number-group">
                    <span class="number blue">
                      {{ prediction.blue_ball }}
                    </span>
                  </div>
                </template>
                <template v-else>
                  <div class="number-group">
                    <span
                      v-for="(num, index) in prediction.front_numbers"
                      :key="'front' + index"
                      class="number red"
                    >
                      {{ num }}
                    </span>
                  </div>
                  <div class="number-group">
                    <span
                      v-for="(num, index) in prediction.back_numbers"
                      :key="'back' + index"
                      class="number blue"
                    >
                      {{ num }}
                    </span>
                  </div>
                </template>
              </div>
              <div class="confidence">
                <el-progress
                  :percentage="prediction.confidence * 100"
                  :color="confidenceColor"
                >
                </el-progress>
                <span class="confidence-text"
                  >预测准确率:
                  {{ (prediction.confidence * 100).toFixed(1) }}%</span
                >
              </div>
              <div class="explanation">
                <h4>预测说明</h4>
                <p>{{ prediction.explanation }}</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="optimization">
            <div slot="header">
              <h3>号码优化</h3>
            </div>
            <div class="optimization-content">
              <el-form :model="optimizationForm" label-width="80px">
                <el-form-item label="选择号码">
                  <el-select
                    v-model="optimizationForm.selectedNumbers"
                    multiple
                    placeholder="请选择号码"
                  >
                    <el-option
                      v-for="num in availableNumbers"
                      :key="num"
                      :label="num"
                      :value="num"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="optimizeNumbers"
                    >优化号码</el-button
                  >
                </el-form-item>
              </el-form>
              <div v-if="optimizedNumbers.length > 0" class="optimized-result">
                <h4>优化结果</h4>
                <div class="number-group">
                  <span
                    v-for="(num, index) in optimizedNumbers"
                    :key="index"
                    class="number"
                  >
                    {{ num }}
                  </span>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 预测趋势 -->
      <el-card class="trend-card">
        <div slot="header">
          <h3>预测趋势</h3>
          <el-radio-group v-model="trendPeriod" size="small">
            <el-radio-button label="week">周</el-radio-button>
            <el-radio-button label="month">月</el-radio-button>
            <el-radio-button label="year">年</el-radio-button>
          </el-radio-group>
        </div>
        <div ref="trendChart" class="trend-chart"></div>
      </el-card>

      <!-- 预测统计 -->
      <el-row :gutter="20" class="statistics-section">
        <el-col :span="8" v-for="(stat, index) in statistics" :key="index">
          <el-card class="stat-card">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'PredictionView',
  data() {
    return {
      currentLottery: 'ssq',
      prediction: {
        red_balls: [1, 7, 12, 23, 28, 33],
        blue_ball: 6,
        front_numbers: [1, 7, 12, 23, 28],
        back_numbers: [6, 12],
        confidence: 0.85,
        explanation:
          '基于历史数据分析，本期号码组合具有较高的中奖概率。红球选择考虑了热温冷号码的平衡，蓝球则根据近期走势选择。',
      },
      optimizationForm: {
        selectedNumbers: [],
      },
      availableNumbers: Array.from({ length: 33 }, (_, i) => i + 1),
      optimizedNumbers: [],
      trendPeriod: 'month',
      trendChart: null,
      statistics: [
        {
          label: '预测准确率',
          value: '85%',
        },
        {
          label: '中奖次数',
          value: '156',
        },
        {
          label: '平均收益',
          value: '2.5倍',
        },
      ],
    }
  },
  computed: {
    confidenceColor() {
      const confidence = this.prediction.confidence
      if (confidence >= 0.8) return '#67C23A'
      if (confidence >= 0.6) return '#E6A23C'
      return '#F56C6C'
    },
  },
  mounted() {
    this.initChart()
    this.fetchPrediction()
    this.updateStatistics()
  },
  beforeDestroy() {
    if (this.trendChart) {
      this.trendChart.dispose()
    }
  },
  methods: {
    /**
     * 初始化图表
     */
    initChart() {
      this.trendChart = echarts.init(this.$refs.trendChart)
      this.updateChart()
    },

    /**
     * 更新图表数据
     */
    updateChart() {
      // 根据选择的时间段生成不同的数据
      let xAxisData = []
      let seriesData = []

      if (this.trendPeriod === 'week') {
        xAxisData = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        seriesData = [75, 82, 78, 85, 88, 85, 80]
      } else if (this.trendPeriod === 'month') {
        xAxisData = ['1月', '2月', '3月', '4月', '5月', '6月']
        seriesData = [70, 75, 80, 85, 82, 78]
      } else { // year
        xAxisData = ['2020年', '2021年', '2022年', '2023年', '2024年']
        seriesData = [65, 70, 75, 80, 85]
      }

      const option = {
        title: {
          text: '预测准确率趋势',
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: xAxisData,
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
        },
        series: [
          {
            name: '准确率',
            type: 'line',
            data: seriesData,
            smooth: true,
            areaStyle: {
              opacity: 0.3,
            },
          },
        ],
      }
      this.trendChart.setOption(option)
    },

    /**
     * 获取预测数据
     */
    async fetchPrediction() {
      try {
        // 模拟数据处理延迟
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 根据彩票类型生成不同的模拟预测数据
        if (this.currentLottery === 'ssq') {
          // 双色球：6个红球(1-33) + 1个蓝球(1-16)
          this.prediction = {
            red_balls: this.generateUniqueRandomNumbers(6, 1, 33).sort((a, b) => a - b),
            blue_ball: this.getRandomInt(1, 16),
            confidence: this.getRandomInt(70, 95) / 100,
            explanation: '基于历史数据分析，本期号码组合具有较高的中奖概率。红球选择考虑了热温冷号码的平衡，蓝球则根据近期走势选择。'
          };
        } else {
          // 大乐透：5个前区号码(1-35) + 2个后区号码(1-12)
          this.prediction = {
            front_numbers: this.generateUniqueRandomNumbers(5, 1, 35).sort((a, b) => a - b),
            back_numbers: this.generateUniqueRandomNumbers(2, 1, 12).sort((a, b) => a - b),
            confidence: this.getRandomInt(70, 95) / 100,
            explanation: '基于近期开奖结果的数据分析，本期号码组合平衡了热号和冷号，考虑了号码分布规律和周期性特征。'
          };
        }
        
        // 更新数据后刷新界面
        this.updateStatistics();
      } catch (error) {
        this.$message.error('获取预测数据失败');
        console.error('获取预测数据失败:', error);
      }
    },
    
    /**
     * 生成指定范围内的随机整数
     */
    getRandomInt(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    
    /**
     * 生成指定数量不重复的随机数
     */
    generateUniqueRandomNumbers(count, min, max) {
      const numbers = new Set();
      while (numbers.size < count) {
        numbers.add(this.getRandomInt(min, max));
      }
      return Array.from(numbers);
    },

    /**
     * 优化号码
     */
    async optimizeNumbers() {
      try {
        // 验证是否选择了号码
        if (this.optimizationForm.selectedNumbers.length === 0) {
          this.$message.warning('请至少选择一个号码');
          return;
        }
        
        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 根据彩票类型和已选择的号码生成优化结果
        const selectedNumbers = this.optimizationForm.selectedNumbers;
        let resultNumbers = [];
        
        if (this.currentLottery === 'ssq') {
          // 双色球：需要6个红球
          // 如果用户选择的号码少于6个，随机补充到6个
          if (selectedNumbers.length < 6) {
            // 找出未被选择的号码
            const remainingNumbers = Array.from({length: 33}, (_, i) => i + 1)
              .filter(num => !selectedNumbers.includes(num));
            
            // 随机从未选择的号码中选取需要补充的数量
            const additionalNumbers = this.getRandomSubset(
              remainingNumbers, 
              6 - selectedNumbers.length
            );
            
            // 合并选择的号码和补充的号码
            resultNumbers = [...selectedNumbers, ...additionalNumbers].sort((a, b) => a - b);
          } else if (selectedNumbers.length > 6) {
            // 如果选择超过6个，随机保留6个
            resultNumbers = this.getRandomSubset(selectedNumbers, 6).sort((a, b) => a - b);
          } else {
            // 刚好6个，直接使用
            resultNumbers = [...selectedNumbers].sort((a, b) => a - b);
          }
        } else {
          // 大乐透：需要5个前区号码
          // 类似逻辑，不过这里是5个号码
          if (selectedNumbers.length < 5) {
            const remainingNumbers = Array.from({length: 35}, (_, i) => i + 1)
              .filter(num => !selectedNumbers.includes(num));
            
            const additionalNumbers = this.getRandomSubset(
              remainingNumbers, 
              5 - selectedNumbers.length
            );
            
            resultNumbers = [...selectedNumbers, ...additionalNumbers].sort((a, b) => a - b);
          } else if (selectedNumbers.length > 5) {
            resultNumbers = this.getRandomSubset(selectedNumbers, 5).sort((a, b) => a - b);
          } else {
            resultNumbers = [...selectedNumbers].sort((a, b) => a - b);
          }
        }
        
        this.optimizedNumbers = resultNumbers;
        this.$message.success('号码优化完成');
      } catch (error) {
        this.$message.error('号码优化失败，请稍后重试');
        console.error('号码优化失败:', error);
      }
    },
    
    /**
     * 从数组中随机选择指定数量的元素
     */
    getRandomSubset(array, count) {
      const shuffled = [...array].sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    },

    /**
     * 更新统计数据
     */
    updateStatistics() {
      // 根据彩票类型和时间段生成不同的统计数据
      let accuracy = '85%'
      let winCount = '156'
      let avgReturn = '2.5倍'

      if (this.currentLottery === 'ssq') {
        if (this.trendPeriod === 'week') {
          accuracy = '87%'
          winCount = '32'
          avgReturn = '2.8倍'
        } else if (this.trendPeriod === 'month') {
          accuracy = '85%'
          winCount = '156'
          avgReturn = '2.5倍'
        } else { // year
          accuracy = '82%'
          winCount = '1872'
          avgReturn = '2.3倍'
        }
      } else { // dlt
        if (this.trendPeriod === 'week') {
          accuracy = '86%'
          winCount = '28'
          avgReturn = '3.0倍'
        } else if (this.trendPeriod === 'month') {
          accuracy = '83%'
          winCount = '142'
          avgReturn = '2.7倍'
        } else { // year
          accuracy = '80%'
          winCount = '1680'
          avgReturn = '2.4倍'
        }
      }

      this.statistics = [
        {
          label: '预测准确率',
          value: accuracy,
        },
        {
          label: '中奖次数',
          value: winCount,
        },
        {
          label: '平均收益',
          value: avgReturn,
        },
      ]
    },
  },
  watch: {
    currentLottery() {
      this.fetchPrediction()
      this.updateStatistics()
    },
    trendPeriod() {
      this.updateChart()
      this.updateStatistics()
    },
  },
}
</script>

<style lang="scss" scoped>
.prediction {
  .prediction-card {
    h2 {
      margin: 0;
      color: #303133;
    }
  }

  .prediction-section {
    margin-bottom: 20px;

    .prediction-result,
    .optimization {
      h3 {
        margin: 0;
        color: #303133;
      }
    }

    .prediction-content {
      .lottery-type {
        margin-bottom: 20px;
      }

      .numbers-display {
        margin-bottom: 20px;

        .number-group {
          display: flex;
          gap: 10px;
          margin-bottom: 10px;

          .number {
            width: 40px;
            height: 40px;
            line-height: 40px;
            text-align: center;
            border-radius: 50%;
            font-weight: bold;
            color: #fff;

            &.red {
              background-color: #f56c6c;
            }

            &.blue {
              background-color: #409eff;
            }
          }
        }
      }

      .confidence {
        margin-bottom: 20px;

        .confidence-text {
          display: block;
          margin-top: 10px;
          text-align: center;
          color: #606266;
        }
      }

      .explanation {
        h4 {
          margin: 0 0 10px;
          color: #303133;
        }

        p {
          margin: 0;
          color: #606266;
          line-height: 1.6;
        }
      }
    }

    .optimization-content {
      .optimized-result {
        margin-top: 20px;

        h4 {
          margin: 0 0 10px;
          color: #303133;
        }

        .number-group {
          display: flex;
          flex-wrap: wrap;
          gap: 10px;

          .number {
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            border-radius: 50%;
            background-color: #409eff;
            color: #fff;
            font-weight: bold;
          }
        }
      }
    }
  }

  .trend-card {
    margin-bottom: 20px;

    .el-card__header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h3 {
        margin: 0;
        color: #303133;
      }
    }

    .trend-chart {
      height: 300px;
    }
  }

  .statistics-section {
    .stat-card {
      text-align: center;
      padding: 20px;

      .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #409eff;
        margin-bottom: 10px;
      }

      .stat-label {
        color: #606266;
      }
    }
  }
}
</style>
