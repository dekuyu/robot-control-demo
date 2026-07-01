// ===== 快捷键注册 Composable =====
import { onMounted, onUnmounted } from 'vue'

interface KeyBinding {
  key: string
  ctrl?: boolean
  handler: () => void
  description: string
}

export function useKeyboard(bindings: KeyBinding[]) {
  function handleKeydown(e: KeyboardEvent) {
    for (const binding of bindings) {
      const ctrlMatch = binding.ctrl ? e.ctrlKey : true
      if (ctrlMatch && e.key.toLowerCase() === binding.key.toLowerCase()) {
        e.preventDefault()
        binding.handler()
      }
    }
  }

  onMounted(() => {
    window.addEventListener('keydown', handleKeydown)
  })

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeydown)
  })

  return { bindings }
}
