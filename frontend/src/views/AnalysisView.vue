<template>
  <div class="analysis">
    <el-card class="analysis-card">
      <div slot="header">
        <h2>数据分析</h2>
      </div>

      <!-- 数据筛选区域 -->
      <el-form :model="filterForm" label-width="120px" class="filter-form">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="彩票类型">
              <el-radio-group v-model="filterForm.lotteryType">
                <el-radio label="ssq">双色球</el-radio>
                <el-radio label="dlt">大乐透</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="日期范围">
              <el-date-picker
                v-model="filterForm.dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
              >
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="期数">
              <el-select v-model="filterForm.periods" placeholder="请选择期数">
                <el-option label="最近10期" :value="10"></el-option>
                <el-option label="最近30期" :value="30"></el-option>
                <el-option label="最近50期" :value="50"></el-option>
                <el-option label="最近100期" :value="100"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询数据</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 图表展示区域 -->
      <el-row :gutter="20" class="chart-container">
        <el-col :span="12">
          <el-card class="chart-card">
            <div slot="header">
              <h3>走势图</h3>
            </div>
            <div ref="trendChart" class="chart"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="chart-card">
            <div slot="header">
              <h3>K线分析</h3>
            </div>
            <div ref="klineChart" class="chart"></div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 预测结果区域 -->
      <el-card class="prediction-card">
        <div slot="header" class="prediction-header">
          <h3>号码预测</h3>
          <el-button
            type="primary"
            @click="getPrediction"
            :loading="predicting"
          >
            获取预测
          </el-button>
        </div>
        <div v-if="prediction" class="prediction-content">
          <div class="prediction-numbers">
            <template v-if="filterForm.lotteryType === 'ssq'">
              <div class="number-group">
                <span class="label">红球：</span>
                <span
                  v-for="(num, index) in prediction.red_balls"
                  :key="index"
                  class="number red"
                >
                  {{ num }}
                </span>
              </div>
              <div class="number-group">
                <span class="label">蓝球：</span>
                <span class="number blue">{{ prediction.blue_ball }}</span>
              </div>
            </template>
            <template v-else>
              <div class="number-group">
                <span class="label">前区：</span>
                <span
                  v-for="(num, index) in prediction.front_numbers"
                  :key="index"
                  class="number red"
                >
                  {{ num }}
                </span>
              </div>
              <div class="number-group">
                <span class="label">后区：</span>
                <span
                  v-for="(num, index) in prediction.back_numbers"
                  :key="index"
                  class="number blue"
                >
                  {{ num }}
                </span>
              </div>
            </template>
          </div>
          <div class="prediction-info">
            <p class="confidence">
              置信度：{{ (prediction.confidence * 100).toFixed(1) }}%
            </p>
            <p class="explanation">{{ prediction.explanation }}</p>
          </div>
        </div>
      </el-card>

      <!-- 历史数据表格 -->
      <el-card class="history-card">
        <div slot="header">
          <h3>历史数据</h3>
        </div>
        <el-table :data="historyData" style="width: 100%">
          <el-table-column
            prop="date"
            label="日期"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="period"
            label="期号"
            width="120"
          ></el-table-column>
          <el-table-column label="红球" min-width="300">
            <template slot-scope="scope">
              <span
                v-for="(num, index) in scope.row.red"
                :key="index"
                class="number red"
              >
                {{ num }}
              </span>
            </template>
          </el-table-column>
          <el-table-column label="蓝球" min-width="150">
            <template slot-scope="scope">
              <span
                v-for="(num, index) in scope.row.blue"
                :key="index"
                class="number blue"
              >
                {{ num }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'AnalysisView',
  data() {
    return {
      filterForm: {
        lotteryType: 'ssq',
        dateRange: [],
        periods: 30,
      },
      historyData: [],
      trendChart: null,
      klineChart: null,
      prediction: null,
      predicting: false,
    }
  },
  mounted() {
    this.initCharts()
    this.fetchData()
  },
  beforeDestroy() {
    // 销毁图表实例
    if (this.trendChart) {
      this.trendChart.dispose()
    }
    if (this.klineChart) {
      this.klineChart.dispose()
    }
  },
  methods: {
    /**
     * 初始化图表
     */
    initCharts() {
      this.trendChart = echarts.init(this.$refs.trendChart)
      this.klineChart = echarts.init(this.$refs.klineChart)
    },

    /**
     * 获取数据
     */
    async fetchData() {
      try {
        const params = {
          type: this.filterForm.lotteryType,
          periods: parseInt(this.filterForm.periods),
        }

        console.log('请求参数:', params);

        // 使用测试数据替代 API 请求
        // 生成模拟数据
        const dates = this.generateDates(this.filterForm.periods);
        const trendData = this.generateTrendData(dates);
        const klineData = this.generateKlineData(dates);
        const statsData = this.generateStatsData();

        // 更新图表
        this.updateCharts({
          trend: trendData,
          kline: klineData,
          statistics: statsData,
        });

        // 更新历史数据
        this.updateHistoryData(trendData, dates);
      } catch (error) {
        this.$message.error('获取数据失败，请稍后重试');
        console.error('获取数据失败:', error);
      }
    },

    /**
     * 生成日期列表
     */
    generateDates(periods) {
      const dates = [];
      const today = new Date();
      
      for (let i = 0; i < periods; i++) {
        const date = new Date();
        date.setDate(today.getDate() - i * 2);
        dates.unshift(this.formatDate(date));
      }
      
      return dates;
    },

    /**
     * 格式化日期
     */
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    /**
     * 生成趋势数据
     */
    generateTrendData(dates) {
      const isSSQ = this.filterForm.lotteryType === 'ssq';
      const data = {
        dates: dates
      };
      
      if (isSSQ) {
        data.red_balls = this.generateRandomNumbers(dates.length, 1, 33);
        data.blue_balls = this.generateRandomNumbers(dates.length, 1, 16);
      } else {
        data.front_numbers = this.generateRandomNumbers(dates.length, 1, 35);
        data.back_numbers = this.generateRandomNumbers(dates.length, 1, 12);
      }
      
      return data;
    },

    /**
     * 生成 K 线数据
     */
    generateKlineData(dates) {
      const values = [];
      
      for (let i = 0; i < dates.length; i++) {
        const min = 1;
        const max = this.filterForm.lotteryType === 'ssq' ? 33 : 35;
        
        const open = this.getRandomInt(min, max);
        const close = this.getRandomInt(min, max);
        const low = Math.min(open, close) - this.getRandomInt(0, 3);
        const high = Math.max(open, close) + this.getRandomInt(0, 3);
        
        values.push({
          open: Math.max(min, open),
          close: Math.max(min, close),
          low: Math.max(min, low),
          high: Math.min(max, high),
          volume: this.getRandomInt(100, 1000)
        });
      }
      
      return {
        dates: dates,
        values: values
      };
    },

    /**
     * 生成统计数据
     */
    generateStatsData() {
      const isSSQ = this.filterForm.lotteryType === 'ssq';
      const data = {};
      
      if (isSSQ) {
        data.red_ball_stats = {
          hot_numbers: this.generateRandomNumbers(3, 1, 33),
          cold_numbers: this.generateRandomNumbers(3, 1, 33),
          frequency: {
            '1-10': this.getRandomInt(20, 40),
            '11-20': this.getRandomInt(30, 50),
            '21-33': this.getRandomInt(20, 40)
          }
        };
        
        data.blue_ball_stats = {
          hot_numbers: this.generateRandomNumbers(3, 1, 16),
          cold_numbers: this.generateRandomNumbers(3, 1, 16),
          frequency: {
            '1-5': this.getRandomInt(20, 40),
            '6-10': this.getRandomInt(30, 50),
            '11-16': this.getRandomInt(20, 40)
          }
        };
      } else {
        data.front_numbers_stats = {
          hot_numbers: this.generateRandomNumbers(3, 1, 35),
          cold_numbers: this.generateRandomNumbers(3, 1, 35),
          frequency: {
            '1-12': this.getRandomInt(20, 40),
            '13-24': this.getRandomInt(30, 50),
            '25-35': this.getRandomInt(20, 40)
          }
        };
        
        data.back_numbers_stats = {
          hot_numbers: this.generateRandomNumbers(3, 1, 12),
          cold_numbers: this.generateRandomNumbers(3, 1, 12),
          frequency: {
            '1-4': this.getRandomInt(20, 40),
            '5-8': this.getRandomInt(30, 50),
            '9-12': this.getRandomInt(20, 40)
          }
        };
      }
      
      return data;
    },

    /**
     * 生成随机数字数组
     */
    generateRandomNumbers(count, min, max) {
      const numbers = [];
      for (let i = 0; i < count; i++) {
        numbers.push(this.getRandomInt(min, max));
      }
      return numbers;
    },

    /**
     * 获取随机整数
     */
    getRandomInt(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    /**
     * 更新历史数据
     */
    updateHistoryData(trendData, dates) {
      const isSSQ = this.filterForm.lotteryType === 'ssq';
      this.historyData = dates.map((date, index) => {
        const period = `2024${String(index + 1).padStart(3, '0')}`;
        
        if (isSSQ) {
          return {
            date: date,
            period: period,
            red: [trendData.red_balls[index]],
            blue: [trendData.blue_balls[index]]
          };
        } else {
          return {
            date: date,
            period: period,
            red: [trendData.front_numbers[index]],
            blue: [trendData.back_numbers[index]]
          };
        }
      });
    },

    /**
     * 更新图表数据
     */
    updateCharts(data) {
      // 更新走势图
      const trendOption = {
        title: {
          text: '号码走势',
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: data.trend.dates,
        },
        yAxis: {
          type: 'value',
        },
        series: [],
      }

      if (this.filterForm.lotteryType === 'ssq') {
        trendOption.series = [
          {
            name: '红球',
            type: 'line',
            data: data.trend.red_balls,
            itemStyle: { color: '#f56c6c' },
          },
          {
            name: '蓝球',
            type: 'line',
            data: data.trend.blue_balls,
            itemStyle: { color: '#409eff' },
          },
        ]
      } else {
        trendOption.series = [
          {
            name: '前区号码',
            type: 'line',
            data: data.trend.front_numbers,
            itemStyle: { color: '#f56c6c' },
          },
          {
            name: '后区号码',
            type: 'line',
            data: data.trend.back_numbers,
            itemStyle: { color: '#409eff' },
          },
        ]
      }

      this.trendChart.setOption(trendOption)

      // 更新K线图
      this.klineChart.setOption({
        title: {
          text: '号码分布',
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
          },
        },
        legend: {
          data: ['号码分布'],
        },
        grid: {
          left: '10%',
          right: '10%',
          bottom: '15%',
        },
        xAxis: {
          type: 'category',
          data: data.kline.dates,
          scale: true,
          boundaryGap: true,
          axisLine: { onZero: false },
          splitLine: { show: false },
          splitNumber: 20,
        },
        yAxis: {
          type: 'value',
          scale: true,
          splitLine: { show: true },
          min: this.filterForm.lotteryType === 'ssq' ? 1 : 1,
          max: this.filterForm.lotteryType === 'ssq' ? 33 : 35,
        },
        dataZoom: [
          {
            type: 'inside',
            start: 0,
            end: 100,
          },
          {
            show: true,
            type: 'slider',
            top: '90%',
            start: 0,
            end: 100,
          },
        ],
        series: [
          {
            name: '号码分布',
            type: 'candlestick',
            data: data.kline.values.map((item) => [
              item.open,
              item.close,
              item.low,
              item.high,
            ]),
            itemStyle: {
              color: '#f56c6c',
              color0: '#409eff',
              borderColor: '#f56c6c',
              borderColor0: '#409eff',
            },
          },
        ],
      })
    },

    /**
     * 重置筛选条件
     */
    resetFilter() {
      this.filterForm = {
        lotteryType: 'ssq',
        dateRange: [],
        periods: 30,
      }
      this.fetchData()
    },

    /**
     * 获取预测数据
     */
    async getPrediction() {
      try {
        this.predicting = true
        const params = {
          type: this.filterForm.lotteryType,
          periods: parseInt(this.filterForm.periods),
        }
        
        console.log('预测请求参数:', params);
        
        // 生成模拟预测数据
        const isSSQ = this.filterForm.lotteryType === 'ssq';
        
        if (isSSQ) {
          this.prediction = {
            red_balls: this.generateRandomNumbers(6, 1, 33).sort((a, b) => a - b),
            blue_ball: this.getRandomInt(1, 16),
            confidence: this.getRandomInt(60, 95) / 100,
            explanation: '基于历史数据频率分析，选择出现次数最多的号码组合。'
          };
        } else {
          this.prediction = {
            front_numbers: this.generateRandomNumbers(5, 1, 35).sort((a, b) => a - b),
            back_numbers: this.generateRandomNumbers(2, 1, 12).sort((a, b) => a - b),
            confidence: this.getRandomInt(60, 95) / 100,
            explanation: '基于历史数据频率分析，选择出现次数最多的号码组合。'
          };
        }
      } catch (error) {
        this.$message.error('获取预测数据失败')
        console.error('获取预测数据失败:', error)
      } finally {
        this.predicting = false
      }
    },
  },
}
</script>

<style lang="scss" scoped>
.analysis {
  .analysis-card {
    h2 {
      margin: 0;
      color: #303133;
    }
  }

  .filter-form {
    margin-bottom: 20px;
  }

  .chart-container {
    margin-bottom: 20px;

    .chart-card {
      h3 {
        margin: 0;
        color: #303133;
      }

      .chart {
        height: 400px;
      }
    }
  }

  .prediction-card {
    margin-top: 20px;

    .prediction-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h3 {
        margin: 0;
        color: #303133;
      }
    }

    .prediction-content {
      padding: 20px;

      .prediction-numbers {
        margin-bottom: 20px;

        .number-group {
          margin-bottom: 15px;

          .label {
            font-size: 16px;
            margin-right: 10px;
          }

          .number {
            display: inline-block;
            width: 36px;
            height: 36px;
            line-height: 36px;
            text-align: center;
            border-radius: 50%;
            margin: 0 5px;
            color: #fff;
            font-weight: bold;
            font-size: 16px;

            &.red {
              background-color: #f56c6c;
            }

            &.blue {
              background-color: #409eff;
            }
          }
        }
      }

      .prediction-info {
        background-color: #f5f7fa;
        padding: 15px;
        border-radius: 4px;

        .confidence {
          font-size: 16px;
          color: #409eff;
          margin: 0 0 10px;
        }

        .explanation {
          color: #606266;
          margin: 0;
        }
      }
    }
  }

  .history-card {
    h3 {
      margin: 0;
      color: #303133;
    }

    .number {
      display: inline-block;
      width: 30px;
      height: 30px;
      line-height: 30px;
      text-align: center;
      border-radius: 50%;
      margin: 0 5px;
      color: #fff;
      font-weight: bold;

      &.red {
        background-color: #f56c6c;
      }

      &.blue {
        background-color: #409eff;
      }
    }
  }
}
</style>
