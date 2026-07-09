<template>
  <div>
    <h2>学生工作台</h2>
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="8">
        <el-card shadow="hover">
          <template #header>快捷操作</template>
          <div class="dash-actions">
            <el-button type="primary" @click="$router.push('/student/exams')">
            查看我的考试
          </el-button>
          <el-button type="success" @click="$router.push('/student/scores')">
            查看我的成绩
          </el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-card shadow="hover">
          <template #header>欢迎</template>
          <p>欢迎使用在线考试系统！您可以参加分配的考试，查看成绩和答题解析。</p>
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