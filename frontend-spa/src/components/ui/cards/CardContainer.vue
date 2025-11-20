<template>
  <div ref="root" class="card3d-container" v-bind="$attrs" @mousemove="onMove" @mouseenter="onEnter" @mouseleave="onLeave">
    <slot />
  </div>
</template>

<script setup>
import { ref, reactive, provide } from 'vue'

const root = ref(null)
const state = reactive({ rotateX: 0, rotateY: 0, entered: false })
const max = 8

function onEnter() { state.entered = true }
function onLeave() { state.entered = false; state.rotateX = 0; state.rotateY = 0 }
function onMove(e) {
  const el = root.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const rx = -((y - rect.height / 2) / rect.height) * max
  const ry = ((x - rect.width / 2) / rect.width) * max
  state.rotateX = rx
  state.rotateY = ry
}

provide('card3d', state)
</script>

<style scoped>
.card3d-container { perspective: 1000px }
</style>