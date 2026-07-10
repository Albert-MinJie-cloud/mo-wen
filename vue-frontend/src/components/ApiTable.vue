<template>
  <div class="api-table-wrapper">
    <table class="api-table">
      <thead>
        <tr>
          <th>参数</th>
          <th>说明</th>
          <th>类型</th>
          <th>默认值</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.name">
          <td class="param-name">{{ row.name }}</td>
          <td class="param-desc">{{ row.desc }}</td>
          <td class="param-type"><code>{{ row.type }}</code></td>
          <td class="param-default"><code>{{ row.default }}</code></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
export interface ApiRow {
  name: string;
  desc: string;
  type: string;
  default: string;
}

defineProps<{
  rows: ApiRow[];
}>();
</script>

<style scoped lang="scss">
.api-table-wrapper {
  margin-bottom: 16px;
  overflow-x: auto;
}

.api-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;

  th {
    text-align: left;
    padding: 10px 16px;
    font-weight: 600;
    color: var(--color-text);
    border-bottom: 2px solid var(--color-border);
    white-space: nowrap;
  }

  td {
    padding: 10px 16px;
    border-bottom: 1px solid var(--color-border-light);
    color: var(--color-text-secondary);
    vertical-align: top;
  }

  tr:last-child td {
    border-bottom: none;
  }

  code {
    background: rgba(255, 255, 255, 0.06);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-family: "SF Mono", "Fira Code", monospace;
    font-size: 13px;
    color: var(--color-accent-cyan-light);
  }
}

.param-name {
  font-weight: 600;
  color: var(--color-text) !important;
}
</style>
