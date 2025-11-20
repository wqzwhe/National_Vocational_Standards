<template>
  <div :class="cls" :style="style">
    <slot />
  </div>
</template>

<script setup>
import { inject, computed } from 'vue'

const props = defineProps({ class: { type: String, default: '' } })
const s = inject('card3d', { rotateX: 0, rotateY: 0, entered: false })

const cls = computed(() => props.class)
const style = computed(() => ({
  transformStyle: 'preserve-3d',
  transform: `rotateX(${s.rotateX}deg) rotateY(${s.rotateY}deg) ${s.entered ? 'scale(1.018)' : 'scale(1.0)'}`,
  transition: s.entered ? 'transform 80ms ease' : 'transform 200ms ease'
}))
</script>

<style scoped>
</style>