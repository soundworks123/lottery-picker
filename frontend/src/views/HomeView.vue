/* eslint-disable */
<template>
  <div class="home">
    <!-- 欢迎卡片 -->
    <el-card class="welcome-card">
      <div class="welcome-content">
        <h1>欢迎使用彩票选号系统</h1>
        <p>本系统提供智能选号、数据分析、专家预测等功能，助您更好地进行彩票选号。</p>
        <el-button type="primary" @click="startLottery">开始选号</el-button>
      </div>
    </el-card>

    <!-- 功能卡片 -->
    <el-row :gutter="20" class="feature-cards">
      <el-col :span="6" v-for="(feature, index) in features" :key="index">
        <el-card class="feature-card">
          <i :class="feature.icon"></i>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 公告卡片 -->
    <el-card class="notice-card">
      <div slot="header">
        <h3>系统公告</h3>
      </div>
      <el-timeline>
        <el-timeline-item
          v-for="(notice, index) in notices"
          :key="index"
          :timestamp="notice.time"
          :type="notice.type"
        >
          {{ notice.content }}
        </el-timeline-item>
      </el-timeline>
    </el-card>

    <!-- 选号技巧 -->
    <el-card class="tips-card">
      <div slot="header">
        <h3>选号技巧</h3>
      </div>
      <el-collapse>
        <el-collapse-item
          v-for="(tip, index) in tips"
          :key="index"
          :title="tip.title"
        >
          <p>{{ tip.content }}</p>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      features: [
        {
          icon: 'el-icon-tickets',
          title: '智能选号',
          description: '基于历史数据和智能算法，为您推荐最优号码组合',
        },
        {
          icon: 'el-icon-data-analysis',
          title: '数据分析',
          description: '深入分析历史数据，发现号码规律和趋势',
        },
        {
          icon: 'el-icon-magic-stick',
          title: '专家预测',
          description: '结合专家经验和机器学习模型，提供专业预测',
        },
        {
          icon: 'el-icon-chat-dot-round',
          title: '用户讨论',
          description: '分享选号经验，交流中奖心得',
        },
      ],
      notices: [
        {
          content: '系统更新：新增智能选号算法，提高预测准确率',
          time: '2024-03-15',
          type: 'primary',
        },
        {
          content: '功能优化：数据分析页面新增K线图表展示',
          time: '2024-03-10',
          type: 'success',
        },
        {
          content: '系统维护：将于本周日凌晨2点进行系统维护',
          time: '2024-03-05',
          type: 'warning',
        },
      ],
      tips: [
        {
          title: '合理控制投注金额',
          content: '建议每次投注金额不超过个人收入的5%，保持理性投注心态。',
        },
        {
          title: '关注历史数据分析',
          content: '通过分析历史数据，了解号码出现规律，提高选号准确性。',
        },
        {
          title: '分散投注策略',
          content: '采用多注号码组合，分散风险，提高中奖机会。',
        },
        {
          title: '保持良好心态',
          content: '彩票投注需要保持平和心态，不要过分追求高额奖金。',
        },
      ],
    }
  },
  methods: {
    startLottery() {
      this.$router.push('/lottery')
    },
  },
}
</script>

<style lang="scss" scoped>
.home {
  .welcome-card {
    margin-bottom: 20px;
    background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
    color: #fff;

    .welcome-content {
      text-align: center;
      padding: 40px 0;

      h1 {
        margin: 0 0 20px;
        font-size: 32px;
      }

      p {
        margin: 0 0 30px;
        font-size: 18px;
      }
    }
  }

  .feature-cards {
    margin-bottom: 20px;

    .feature-card {
      text-align: center;
      padding: 20px;

      i {
        font-size: 48px;
        color: #409eff;
        margin-bottom: 15px;
      }

      h3 {
        margin: 0 0 10px;
        color: #303133;
      }

      p {
        margin: 0;
        color: #606266;
      }
    }
  }

  .notice-card,
  .tips-card {
    margin-bottom: 20px;

    h3 {
      margin: 0;
      color: #303133;
    }
  }

  .tips-card {
    .el-collapse-item {
      p {
        margin: 0;
        color: #606266;
        line-height: 1.6;
      }
    }
  }
}
</style>
