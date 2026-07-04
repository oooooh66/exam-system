<template>
  <div class="not-found">
    <div class="not-found-content">
      <h1>404</h1>
      <p>页面不存在</p>
      <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * 404 页面
 */
</script>

<style scoped>
.not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.not-found-content {
  text-align: center;
}

.not-found-content h1 {
  font-size: 120px;
  color: #dcdfe6;
  line-height: 1;
  margin-bottom: 16px;
}

.not-found-content p {
  font-size: 16px;
  color: #909399;
  margin-bottom: 24px;
}
</style>
