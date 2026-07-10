<template>
  <div :class="['logo', `logo--${size}`]">
    <img src="@/assets/mowen.svg" alt="Logo" class="logo-img" />
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    size?: "sm" | "md" | "lg";
  }>(),
  {
    size: "sm",
  },
);
</script>

<style scoped lang="scss">
.logo {
  display: flex;
  align-items: center;
}

.logo-img {
  object-fit: contain;
}

.logo--sm .logo-img {
  width: 36px;
  height: 36px;
}

.logo--md .logo-img {
  width: 72px;
  height: 72px;
}

.logo--lg .logo-img {
  width: 108px;
  height: 108px;
}
</style>
