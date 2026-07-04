<template>
  <div>
    <h2>教师工作台</h2>
    <el-row :gutter="20" style="margin-top:20px" justify="center">
      <el-col :span="8">
        <el-card shadow="hover" class="dash-card">
          <template #header>快捷操作</template>
          <div class="dash-actions">
            <el-button type="success" @click="$router.push('/admin/questions')">题库管理</el-button>
            <el-button type="warning" @click="$router.push('/admin/papers')">试卷管理</el-button>
            <el-button type="primary" @click="$router.push('/admin/exams')">考试管理</el-button>
            <el-button type="danger" @click="$router.push('/admin/reports')">成绩统计</el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>欢迎</template>
          <p>欢迎使用在线考试系统！您可以管理题库、创建试卷、发布考试、查看成绩统计。</p>
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
