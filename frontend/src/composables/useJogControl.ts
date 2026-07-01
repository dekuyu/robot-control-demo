// ===== 点动控制（按住/释放逻辑） Composable =====
import { ref } from 'vue'
import { controlAPI } from '@/api/control'
import { useControlStore } from '@/stores/control'

export function useJogControl() {
  const controlStore = useControlStore()
  const activeAxis = ref<number | null>(null)

  /** 开始点动（按住触发） */
  async function startJog(axis: number, direction: 'positive' | 'negative') {
    activeAxis.value = axis
    controlStore.setJogging(axis, true)
    try {
      await controlAPI.jogStart({
        axis,
        direction,
        speedPercent: controlStore.actualSpeed,
      })
    } catch {
      activeAxis.value = null
      controlStore.setJogging(axis, false)
    }
  }

  /** 停止点动（松开触发） */
  async function stopJog(axis: number) {
    if (activeAxis.value === axis) {
      activeAxis.value = null
    }
    controlStore.setJogging(axis, false)
    try {
      await controlAPI.jogStop(axis)
    } catch {
      // 忽略停止错误
    }
  }

  return { activeAxis, startJog, stopJog }
}
