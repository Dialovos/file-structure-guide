<template>
  <main>
    <h1>My App</h1>
    <p>Edit <code>pages/index.vue</code> to start.</p>
    <BaseButton @click="onClick">Click me</BaseButton>
    <p v-if="user">Signed in as {{ user.email }}</p>
  </main>
</template>

<script setup lang="ts">
// BaseButton is auto-imported from ~/components/BaseButton.vue.
// useAuth is auto-imported from ~/composables/useAuth.ts.
const { user, signIn } = useAuth();

function onClick() {
  signIn("demo@example.com");
}
</script>
