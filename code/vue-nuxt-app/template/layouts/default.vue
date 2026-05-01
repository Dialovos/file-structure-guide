<template>
  <div class="app-layout">
    <header>
      <nav>
        <NuxtLink to="/">Home</NuxtLink>
        <NuxtLink to="/about">About</NuxtLink>
      </nav>
    </header>
    <slot />
    <footer>
      <small>&copy; My App</small>
    </footer>
  </div>
</template>

<style scoped>
.app-layout {
  max-width: 60rem;
  margin: 0 auto;
  padding: 1rem;
}

nav a {
  margin-right: 1rem;
}
</style>
