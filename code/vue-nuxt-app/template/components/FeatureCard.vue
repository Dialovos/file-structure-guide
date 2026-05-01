<template>
  <article class="feature-card">
    <h3>{{ title }}</h3>
    <p>{{ description }}</p>
    <slot name="footer" />
  </article>
</template>

<script setup lang="ts">
defineProps<{
  title: string;
  description: string;
}>();
</script>

<style scoped>
.feature-card {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 0.25rem;
}
</style>
