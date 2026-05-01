<template>
  <button class="base-button" :type="type" @click="$emit('click', $event)">
    <slot />
  </button>
</template>

<script setup lang="ts">
// Auto-imported as <BaseButton /> in any template, no import needed.
defineProps<{
  type?: "button" | "submit" | "reset";
}>();

defineEmits<{
  click: [event: MouseEvent];
}>();
</script>

<style scoped>
.base-button {
  padding: 0.5rem 1rem;
  border: 1px solid currentColor;
  background: transparent;
  cursor: pointer;
}
</style>
