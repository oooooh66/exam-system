<template>
  <el-table :data="list" size="small" stripe max-height="420">
    <el-table-column label="排名" width="60">
      <template #default="{ $index }">{{ $index + 1 }}</template>
    </el-table-column>
    <el-table-column prop="student_name" label="姓名" min-width="90" />
    <el-table-column prop="org_nm" label="村行" min-width="100" />
    <el-table-column prop="total_score" label="基础分" width="80" align="center" />
    <el-table-column label="浮动分" width="100" align="center">
      <template #default="{ row }">
        <span :style="{ color: (row.float_score||0) >= 0 ? '#67c23a' : '#f56c6c' }">
          {{ (row.float_score||0) >= 0 ? '+' : '' }}{{ row.float_score || 0 }}
        </span>
      </template>
    </el-table-column>
    <el-table-column label="最终得分" width="100" align="center">
      <template #default="{ row }">
        <b style="color:#409eff;font-size:14px">{{ (row.final_score || 0).toFixed(1) }}</b>
      </template>
    </el-table-column>
    <el-table-column prop="submit_time" label="提交时间" width="140" />
    <el-table-column label="操作" width="80" align="center">
      <template #default="{ row }">
        <el-button size="small" @click="$emit('adjust', row)">调分</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
defineProps<{ list: any[] }>()
defineEmits(['adjust'])
</script>
