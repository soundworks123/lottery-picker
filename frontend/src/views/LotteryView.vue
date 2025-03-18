<template>
  <div class="lottery">
    <el-card class="lottery-card">
      <div slot="header">
        <h2>智能选号</h2>
        <div class="lottery-rules">
          <p v-if="form.lotteryType === 'ssq'">
            双色球规则：从1-33中选择6个红球，从1-16中选择1个蓝球
          </p>
          <p v-else>
            大乐透规则：从1-35中选择5个前区号码，从1-12中选择2个后区号码
          </p>
        </div>
      </div>

      <!-- 测试按钮 -->
      <el-button @click="testConnection" type="warning" style="margin-bottom: 20px;">测试后端连接</el-button>

      <!-- 选号表单 -->
      <el-form :model="form" label-width="120px" class="lottery-form">
        <!-- 彩票类型 -->
        <el-form-item label="彩票类型">
          <el-radio-group v-model="form.lotteryType">
            <el-radio label="ssq">双色球</el-radio>
            <el-radio label="dlt">大乐透</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 选号方式 -->
        <el-form-item label="选号方式">
          <el-radio-group v-model="form.selectionType">
            <el-radio label="random">随机选号</el-radio>
            <el-radio label="smart">智能选号</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 选号数量 -->
        <el-form-item label="选号数量">
          <el-input-number
            v-model="form.numberOfSelections"
            :min="1"
            :max="10"
            size="small"
          >
          </el-input-number>
        </el-form-item>

        <!-- 选号类型 -->
        <el-form-item label="选号类型">
          <el-radio-group v-model="form.selectionMode">
            <el-radio label="single">单式</el-radio>
            <el-radio label="multiple">复式</el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- 选号按钮 -->
        <el-form-item>
          <el-button type="primary" @click="generateNumbers"
            >生成号码</el-button
          >
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 号码展示区域 -->
      <div v-if="numbers.length > 0" class="numbers-display">
        <h3>选号结果</h3>
        <div
          v-for="(numberSet, index) in numbers"
          :key="index"
          class="number-set"
        >
          <!-- 双色球显示 -->
          <template v-if="form.lotteryType === 'ssq'">
            <div class="number-group">
              <span
                v-for="(num, idx) in numberSet.red"
                :key="'red' + idx"
                class="number red"
              >
                {{ num }}
              </span>
            </div>
            <div class="number-group">
              <span class="number blue">
                {{ numberSet.blue }}
              </span>
            </div>
          </template>

          <!-- 大乐透显示 -->
          <template v-else>
            <div class="number-group">
              <span
                v-for="(num, idx) in numberSet.front"
                :key="'front' + idx"
                class="number red"
              >
                {{ num }}
              </span>
            </div>
            <div class="number-group">
              <span
                v-for="(num, idx) in numberSet.back"
                :key="'back' + idx"
                class="number blue"
              >
                {{ num }}
              </span>
            </div>
          </template>

          <div v-if="numberSet.confidence" class="number-info">
            <p>置信度：{{ numberSet.confidence }}%</p>
            <p>说明：{{ numberSet.explanation }}</p>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'LotteryView',
  data() {
    return {
      form: {
        lotteryType: 'ssq',
        selectionType: 'random',
        numberOfSelections: 1,
        selectionMode: 'single',
      },
      numbers: [],
    }
  },
  methods: {
    /**
     * 测试后端连接
     */
    async testConnection() {
      try {
        const response = await this.$http.get('/api/lottery/test')
        console.log('测试响应:', response)
        this.$message.success(`测试成功: ${response.message}`)
      } catch (error) {
        console.error('测试失败:', error)
        this.$message.error('测试失败：无法连接到后端服务')
      }
    },

    /**
     * 生成号码
     */
    async generateNumbers() {
      try {
        const selectionType = this.form.selectionType === 'random' ? 'random' : 'smart';
        console.log('请求参数:', {
          type: this.form.lotteryType,
          count: this.form.numberOfSelections,
          mode: this.form.selectionMode,
          selectionType
        });
        
        // 使用本地模拟数据替代API请求
        console.log('使用本地模拟数据生成号码');
        
        // 模拟数据处理延迟
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 根据彩票类型和选号方式生成模拟数据
        const numbers = [];
        const count = this.form.numberOfSelections;
        
        for (let i = 0; i < count; i++) {
          if (this.form.lotteryType === 'ssq') {
            // 双色球：6个红球(1-33) + 1个蓝球(1-16)
            const red_balls = this.generateUniqueRandomNumbers(6, 1, 33);
            const blue_ball = this.getRandomInt(1, 16);
            
            numbers.push({
              red_balls: red_balls.sort((a, b) => a - b),
              blue_ball: blue_ball,
              confidence: this.form.selectionType === 'smart' ? this.getRandomInt(60, 95) : undefined,
              explanation: this.form.selectionType === 'smart' ? '基于历史数据分析，选择了较为均衡的号码组合。' : undefined
            });
          } else {
            // 大乐透：5个前区号码(1-35) + 2个后区号码(1-12)
            const front_numbers = this.generateUniqueRandomNumbers(5, 1, 35);
            const back_numbers = this.generateUniqueRandomNumbers(2, 1, 12);
            
            numbers.push({
              front_numbers: front_numbers.sort((a, b) => a - b),
              back_numbers: back_numbers.sort((a, b) => a - b),
              confidence: this.form.selectionType === 'smart' ? this.getRandomInt(60, 95) : undefined,
              explanation: this.form.selectionType === 'smart' ? '根据近期开奖趋势，选择了热温冷号码搭配的组合。' : undefined
            });
          }
        }
        
        console.log('生成的模拟号码:', numbers);
        
        if (this.form.lotteryType === 'ssq') {
          this.numbers = numbers.map((item) => ({
            red: item.red_balls,
            blue: item.blue_ball,
            confidence: item.confidence,
            explanation: item.explanation,
          }));
        } else {
          this.numbers = numbers.map((item) => ({
            front: item.front_numbers,
            back: item.back_numbers,
            confidence: item.confidence,
            explanation: item.explanation,
          }));
        }
      } catch (error) {
        console.error('生成号码失败:', error);
        this.$message.error('生成号码失败，请稍后重试');
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
     * 重置表单
     */
    resetForm() {
      this.form = {
        lotteryType: 'ssq',
        selectionType: 'random',
        numberOfSelections: 1,
        selectionMode: 'single',
      }
      this.numbers = []
    },
  },
}
</script>

<style lang="scss" scoped>
.lottery {
  .lottery-card {
    max-width: 800px;
    margin: 0 auto;

    h2 {
      margin: 0;
      color: #303133;
    }

    .lottery-rules {
      margin-top: 10px;
      font-size: 14px;
      color: #606266;

      p {
        margin: 5px 0;
      }
    }
  }

  .lottery-form {
    margin-bottom: 30px;
  }

  .numbers-display {
    h3 {
      margin: 0 0 20px;
      color: #303133;
    }

    .number-set {
      display: flex;
      flex-direction: column;
      align-items: center;
      margin-bottom: 20px;
      padding: 20px;
      border: 1px solid #ebeef5;
      border-radius: 4px;
      background-color: #fafafa;

      .number-group {
        display: flex;
        gap: 10px;
        margin: 0 10px 15px;
        padding: 10px;
        background-color: #fff;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

        .number {
          width: 40px;
          height: 40px;
          line-height: 40px;
          text-align: center;
          border-radius: 50%;
          font-weight: bold;
          color: #fff;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

          &.red {
            background-color: #f56c6c;
          }

          &.blue {
            background-color: #409eff;
          }
        }
      }

      .number-info {
        text-align: center;
        color: #606266;
        font-size: 14px;
        padding: 10px;
        background-color: #fff;
        border-radius: 4px;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);

        p {
          margin: 5px 0;
        }
      }
    }
  }
}
</style>
