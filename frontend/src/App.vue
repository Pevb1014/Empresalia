<script setup lang="ts">
import AppNavbar from "@/components/AppNavbar.vue";
</script>

<template>
  <AppNavbar />

  <main>
    <RouterView />
  </main>
</template>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

main {
  padding: 1rem;
}
</style>