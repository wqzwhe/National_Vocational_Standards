<template>
  <component :is="as" :class="cls" :style="style">
    <slot />
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  as: { type: String, default: 'div' },
  translateZ: { type: [String, Number], default: 0 },
  class: { type: String, default: '' }
})

const cls = computed(() => props.class)
const style = computed(() => ({ transform: `translateZ(${Number(props.translateZ)}px)` }))
</script>

<style scoped>
</style>