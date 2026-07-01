<!-- 位置卡片组件 -->
<template>
  <div class="position-card" @click="$emit('select', position)">
    <div class="card-header">
      <h5 class="pos-name">{{ position.name }}</h5>
      <el-dropdown trigger="click" @command="handleCommand">
        <el-button text size="small"><el-icon><MoreFilled /></el-icon></el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="edit">编辑</el-dropdown-item>
            <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
    <p v-if="position.description" class="pos-desc">{{ position.description }}</p>
    <div class="pos-joints">
      <span v-for="(val, key) in joints" :key="key" class="joint-tag">
        {{ key }}: {{ (val as number).toFixed(1) }}°
      </span>
    </div>
    <div class="card-footer">
      <span class="pos-date">{{ formatDateTime(position.createdAt) }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { SavedPosition } from '@/types/position'
import { formatDateTime } from '@/utils/format'

const props = defineProps<{ position: SavedPosition }>()

const emit = defineEmits<{ select: [pos: SavedPosition]; edit: [pos: SavedPosition]; delete: [pos: SavedPosition] }>()

const joints = computed(() => props.position.posture?.joints ?? {})

function handleCommand(cmd: string) {
  if (cmd === 'edit') emit('edit', props.position)
  else if (cmd === 'delete') emit('delete', props.position)
}
</script>

<style scoped lang="scss">
.position-card {
  background: $color-bg-card;
  border: 1px solid $color-border;
  border-radius: $radius-lg;
  padding: $spacing-md;
  cursor: pointer;
  transition: all $transition-fast;
  &:hover { border-color: $color-info; box-shadow: $shadow-card; }
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-sm;
}
.pos-name {
  font-size: 14px;
  font-weight: 600;
  color: $color-text-primary;
  margin: 0;
}
.pos-desc {
  font-size: 12px;
  color: $color-text-secondary;
  margin: 0 0 $spacing-sm;
}
.pos-joints {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: $spacing-sm;
}
.joint-tag {
  font-size: 10px;
  font-family: $font-family-mono;
  color: $color-text-secondary;
  background: rgba($color-bg-input, 0.6);
  padding: 2px 6px;
  border-radius: $radius-sm;
}
.card-footer {
  display: flex;
  justify-content: flex-end;
}
.pos-date {
  font-size: 10px;
  color: $color-text-muted;
}
</style>
