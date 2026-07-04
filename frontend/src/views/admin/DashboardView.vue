<template>
  <div class="dashboard">
    <h2>管理员工作台</h2>
    <el-row :gutter="20" style="margin-top:20px" justify="center">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>快捷操作</template>
          <div class="dash-actions">
            <el-button type="primary" @click="$router.push('/admin/users')">用户管理</el-button>
            <el-button type="success" @click="$router.push('/admin/questions')">题库管理</el-button>
            <el-button type="warning" @click="$router.push('/admin/papers')">试卷管理</el-button>
            <el-button type="danger" @click="$router.push('/admin/reports')">成绩报表</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>系统概览</template>
          <p>欢迎使用在线考试系统！使用左侧菜单进行各项管理操作。</p>
          <p>账号：admin / admin123, teacher / teacher123, student / student123</p>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.dash-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.dash-actions .el-button {
  width: 100%;
  margin-left: 0px;
}
</style>
