<template>
  <a-layout-footer class="footer">
    <div class="footer-content">
      <p class="copyright">
        &copy; 2026 minjie. All rights reserved.<span class="version">V{{ version }}</span>
      </p>
    </div>
  </a-layout-footer>
</template>

<script setup lang="ts">
import { version } from "../../package.json";
</script>

<style scoped>
.footer {
  background: var(--color-background);
  text-align: center;
  padding: 24px 20px;
  margin-top: 0;
  border-top: 1px solid var(--color-border);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

.copyright {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 13px;

  .version {
    color: var(--color-primary-light);
    margin-left: 8px;
    font-weight: 500;
  }
}


</style>
