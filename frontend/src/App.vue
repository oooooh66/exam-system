<template>
  <router-view />
</template>

<script setup lang="ts">
/**
 * 在线考试系统 - 根组件
 * 通过 router-view 根据路由渲染不同页面
 */
</script>

<style>
/* 全局重置样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  width: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
    'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
}
</style>
