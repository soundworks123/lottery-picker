<template>
  <div class="nav-menu">
    <el-row type="flex" justify="center" align="middle">
      <el-col :span="20">
        <el-menu
          :router="true"
          mode="horizontal"
          :default-active="activeRoute"
          class="main-menu"
        >
          <el-menu-item index="/">
            <i class="el-icon-s-home"></i>
            首页
          </el-menu-item>
          <el-menu-item index="/lottery">
            <i class="el-icon-s-opportunity"></i>
            智能选号
          </el-menu-item>
          <el-menu-item index="/analysis">
            <i class="el-icon-s-data"></i>
            数据分析
          </el-menu-item>
          <el-menu-item index="/prediction">
            <i class="el-icon-s-marketing"></i>
            预测系统
          </el-menu-item>
          <el-menu-item index="/discussion">
            <i class="el-icon-s-comment"></i>
            讨论区
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'NavMenu',
  computed: {
    activeRoute() {
      return this.$route.path
    }
  }
}
</script>

<style lang="scss" scoped>
.nav-menu {
  .main-menu {
    display: flex;
    justify-content: center;
    border-bottom: none;
    
    .el-menu-item {
      height: 60px;
      line-height: 60px;
      font-size: 16px;
      
      i {
        margin-right: 5px;
        font-size: 18px;
      }
      
      &:hover, &:focus {
        background-color: #f5f7fa;
      }
      
      &.is-active {
        color: #409EFF;
        border-bottom: 2px solid #409EFF;
      }
    }
  }
}
</style>
