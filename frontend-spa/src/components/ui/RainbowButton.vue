<template>
  <button
    :type="type"
    :disabled="disabled"
    v-bind="$attrs"
    :class="classes"
    @click="onClick"
  >
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false },
  type: { type: String, default: 'button' },
  size: { type: String, default: 'md' }
})

const emit = defineEmits(['click'])

const sizeClass = computed(() => {
  if (props.size === 'sm') return 'px-2.5 py-1.5 text-xs'
  if (props.size === 'lg') return 'px-6 py-3 text-base'
  return 'px-3.5 py-2.5 text-sm'
})

const classes = computed(() => [
  'inline-flex items-center justify-center rounded-lg bg-gradient-to-r from-fuchsia-600 via-rose-500 to-orange-400 text-white shadow-lg transition duration-200 ease-out hover:brightness-110 hover:-translate-y-0.5 disabled:opacity-60',
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-500',
  'dark:shadow-indigo-900/40',
  sizeClass.value
])

function onClick(e) {
  if (props.disabled) return
  emit('click', e)
}
</script>

<style scoped>
</style>