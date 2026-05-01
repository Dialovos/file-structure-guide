// Nuxt 3 config. The defineNuxtConfig helper gives you typed config and
// editor autocomplete. Add modules, runtime config, and build options here.
//
// Reference: https://nuxt.com/docs/api/configuration/nuxt-config

export default defineNuxtConfig({
  devtools: { enabled: true },
  typescript: {
    strict: true,
  },
  css: [
    // "~/assets/styles/main.css",
  ],
  modules: [
    // Add Nuxt modules here, e.g. "@pinia/nuxt", "@nuxt/image".
  ],
});
