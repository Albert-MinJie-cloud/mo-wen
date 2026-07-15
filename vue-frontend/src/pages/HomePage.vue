<script setup lang="ts">
import HeroSection from "@/components/HeroSection.vue";
import EditorMockup from "@/components/EditorMockup.vue";
import FeaturesSection from "@/components/FeaturesSection.vue";
</script>

<template>
  <div id="homePage">
    <HeroSection />
    <EditorMockup />
    <FeaturesSection />
  </div>
</template>

<style scoped>
#homePage {
  width: 100%;
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background: var(--color-background);
}
</style>
