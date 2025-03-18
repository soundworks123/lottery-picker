<template>
  <div id="app">
    <el-container>
      <el-header>
        <nav-menu></nav-menu>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
      <el-footer>
        <footer-component></footer-component>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import NavMenu from '@/components/NavMenu.vue'
import FooterComponent from '@/components/FooterComponent.vue'

export default {
  name: 'App',
  components: {
    NavMenu,
    FooterComponent,
  },
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  padding: 0;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
}

.el-footer {
  padding: 20px;
  background-color: #fff;
  text-align: center;
  color: #909399;
}
</style>
