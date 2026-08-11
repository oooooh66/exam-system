<template>
  <el-table :data="list" stripe size="small" style="width:100%;font-size:13px">
    <el-table-column label="#" width="40" align="center">
      <template #default="{ $index }">{{ $index + 1 }}</template>
    </el-table-column>
    <el-table-column prop="org_no" label="机构号" width="80" align="center" />
    <el-table-column prop="org_nm" label="机构名" min-width="80" show-overflow-tooltip />
    <el-table-column prop="student_username" label="账号" width="90" align="center" />
    <el-table-column prop="student_name" label="姓名" min-width="60" show-overflow-tooltip />
    <el-table-column prop="total_score" label="考试分" width="70" align="center" />
    <el-table-column label="浮动分" width="70" align="center">
      <template #default="{ row }">
        <span :style="{ color: (row.float_score || 0) >= 0 ? '#67c23a' : '#f56c6c', fontWeight: 600 }">
          {{ (row.float_score || 0) >= 0 ? '+' : '' }}{{ row.float_score || 0 }}
        </span>
      </template>
    </el-table-column>
    <el-table-column label="总分" width="70" align="center">
      <template #default="{ row }">
        <b style="color:#409eff">{{ (row.final_score || 0).toFixed(1) }}</b>
      </template>
    </el-table-column>
    <el-table-column prop="adjusted_by" label="打分人" width="100" show-overflow-tooltip />
    <el-table-column prop="adjusted_at" label="打分时间" width="140" />
    <el-table-column prop="submit_time" label="提交时间" width="140" />
    <el-table-column label="状态" width="70" align="center">
      <template #default="{ row }">
        <el-tag :type="statusTag(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
      </template>
    </el-table-column>
    <el-table-column label="操作" width="70" align="center" fixed="right">
      <template #default="{ row }">
        <el-button
          v-if="floatEnabled && (isAdmin || row.float_score === null || row.float_score === undefined)"
          size="small" type="warning" style="font-size:12px" @click="$emit('adjust', row)"
        >浮动分</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script setup lang="ts">
defineProps<{ list: any[]; floatEnabled: boolean; isAdmin?: boolean }>()
defineEmits(['adjust'])

function statusTag(s: string) {
  return { submitted: 'success', auto_submitted: 'warning', in_progress: 'info' }[s] || 'info'
}
function statusText(s: string) {
  return { submitted: '正常', auto_submitted: '自动', in_progress: '答题中', not_started: '未开始' }[s] || s
}
</script>