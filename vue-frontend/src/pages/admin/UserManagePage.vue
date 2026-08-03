<template>
  <div id="userManagePage">
    <PageHeader title="用户管理" subtitle="管理系统中的所有用户" />

    <div class="container">
      <a-card :bordered="false" class="content-card">
        <!-- 搜索表单 -->
        <div class="search-section">
          <a-form
            layout="inline"
            :model="searchParams"
            @finish="doSearch"
            class="search-form"
          >
            <a-form-item label="账号">
              <a-input
                v-model:value="searchParams.userAccount"
                placeholder="输入账号"
                class="search-input"
              />
            </a-form-item>
            <a-form-item label="用户名">
              <a-input
                v-model:value="searchParams.userName"
                placeholder="输入用户名"
                class="search-input"
              />
            </a-form-item>
            <a-form-item>
              <Button variant="secondary" native-type="submit" size="sm">
                <SearchOutlined />
                搜索
              </Button>
            </a-form-item>
          </a-form>
        </div>

        <a-divider />

        <!-- 表格 -->
        <a-table
          :columns="columns"
          :data-source="data"
          :pagination="pagination"
          @change="doTableChange"
          class="user-table"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.dataIndex === 'userAvatar'">
              <a-avatar
                :src="record.userAvatar"
                :size="48"
                class="user-avatar"
              />
            </template>
            <template v-else-if="column.dataIndex === 'userRole'">
              <a-tag
                v-if="record.userRole === 'admin'"
                color="purple"
                class="role-tag"
              >
                管理员
              </a-tag>
              <a-tag v-else color="blue" class="role-tag"> 普通用户 </a-tag>
            </template>
            <template v-else-if="column.dataIndex === 'createTime'">
              <span class="time-text">{{
                formatTime(record.createTime, "YYYY-MM-DD HH:mm:ss")
              }}</span>
            </template>
            <template v-else-if="column.key === 'action'">
              <a-popconfirm
                title="确定要删除此用户吗?"
                ok-text="确定"
                cancel-text="取消"
                @confirm="doDelete(record.id)"
              >
                <a-button type="link" danger class="delete-btn">删除</a-button>
              </a-popconfirm>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>
  </div>
</template>
<script lang="ts" setup>
import { computed, onMounted, reactive, ref } from "vue";
import { deleteUserApiUserDeletePost, listUsersByPageApiUserListPagePost } from "@/api/user";
import { message } from "@/message";
import { SearchOutlined } from "@ant-design/icons-vue";
import Button from "@/components/Button.vue";
import PageHeader from "@/components/PageHeader.vue";
import { formatTime } from "@/utils/format";

const columns = [
  {
    title: "id",
    dataIndex: "id",
  },
  {
    title: "账号",
    dataIndex: "userAccount",
  },
  {
    title: "用户名",
    dataIndex: "userName",
  },
  {
    title: "头像",
    dataIndex: "userAvatar",
  },
  {
    title: "用户角色",
    dataIndex: "userRole",
  },
  {
    title: "创建时间",
    dataIndex: "createTime",
  },
  {
    title: "操作",
    key: "action",
  },
];

// 展示的数据
const data = ref<API.UserVO[]>([]);
const total = ref(0);

// 搜索条件
const searchParams = reactive<API.UserQueryRequest>({
  current: 1,
  pageSize: 10,
});

// 获取数据
const fetchData = async () => {
  const res = await listUsersByPageApiUserListPagePost({}, {
    ...searchParams,
  });
  if (res.data.data) {
    data.value = res.data.data.records ?? [];
    total.value = res.data.data.total ?? 0;
  } else {
    message.error("获取数据失败，" + res.data.message);
  }
};

// 分页参数
const pagination = computed(() => {
  return {
    current: searchParams.current ?? 1,
    pageSize: searchParams.pageSize ?? 10,
    total: total.value,
    showSizeChanger: true,
    showTotal: (total: number) => `共 ${total} 条`,
  };
});

// 表格分页变化时的操作
const doTableChange = (page: { current: number; pageSize: number }) => {
  searchParams.current = page.current;
  searchParams.pageSize = page.pageSize;
  fetchData();
};

// 搜索数据
const doSearch = () => {
  // 重置页码
  searchParams.current = 1;
  fetchData();
};

// 删除数据
const doDelete = async (id: number) => {
  if (!id) {
    return;
  }
  const res = await deleteUserApiUserDeletePost({}, { id });
  if (res.data.code === 0) {
    message.success("删除成功");
    // 刷新数据
    fetchData();
  } else {
    message.error("删除失败");
  }
};

// 页面加载时请求一次
onMounted(() => {
  fetchData();
});
</script>

<style scoped lang="scss">
#userManagePage {
  background: var(--color-background-secondary);
  min-height: 100vh;
  padding-bottom: 60px;

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .content-card {
    border-radius: var(--radius-lg);
    border: 1px solid var(--color-border);
    box-shadow: var(--shadow-sm);
    background: var(--color-background);
    overflow: hidden;

    :deep(.ant-card-body) {
      padding: 24px;
      background: var(--color-background);
    }
  }

  .search-section {
    margin-bottom: 8px;
  }

  .search-form {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: flex-end;

    :deep(.ant-form-item) {
      margin-bottom: 0;
    }

    :deep(.ant-form-item-label > label) {
      font-weight: 500;
      font-size: 13px;
      color: var(--color-text-secondary);
    }
  }

  .search-input {
    width: 180px;
    background: var(--color-fill-tertiary) !important;
    border-color: var(--color-border) !important;
    color: var(--color-text) !important;
    border-radius: var(--radius-md);
    font-size: 14px;

    &::placeholder {
      color: var(--color-text-muted);
    }

    &:hover {
      border-color: var(--color-fill) !important;
    }

    &:focus,
    &.ant-input-focused {
      border-color: var(--color-primary) !important;
      box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
      background: var(--color-fill-tertiary) !important;
    }
  }

  .user-table {
    :deep(table),
    :deep(.ant-table-wrapper),
    :deep(.ant-spin-nested-loading),
    :deep(.ant-spin-container),
    :deep(.ant-table),
    :deep(.ant-table-container),
    :deep(.ant-table-content),
    :deep(.ant-table-body) {
      background: transparent;
    }

    :deep(.ant-table-thead > tr > th) {
      background: var(--color-background-secondary);
      font-weight: 600;
      font-size: 13px;
      color: var(--color-text);
      border-bottom: 1px solid var(--color-border) !important;
      padding: 12px 16px;

      &::before {
        display: none !important;
      }
    }

    :deep(.ant-table-cell) {
      box-shadow: none !important;
    }

    :deep(.ant-table-tbody > tr > td) {
      padding: 14px 16px;
      border: none !important;
      color: var(--color-text);
      background: transparent;
      transition: background 0.15s ease;
    }

    :deep(.ant-table-tbody > tr:hover > td) {
      background: rgba(59, 130, 246, 0.04) !important;
    }

    // 分页
    :deep(.ant-pagination-item),
    :deep(.ant-pagination-prev .ant-pagination-item-link),
    :deep(.ant-pagination-next .ant-pagination-item-link) {
      background: var(--color-background);
      border-color: var(--color-border);
      border-radius: var(--radius-sm);

      a { color: var(--color-text-secondary); }

      &:hover {
        border-color: var(--color-primary);
        a { color: var(--color-primary); }
      }
    }

    :deep(.ant-pagination-item-active) {
      background: var(--color-primary);
      border-color: var(--color-primary);

      a { color: #fff; }
      &:hover a { color: #fff; }
    }

    :deep(.ant-pagination-disabled .ant-pagination-item-link) {
      color: var(--color-text-muted);
      background: transparent;
      border-color: var(--color-border-light);
    }

    :deep(.ant-pagination-options .ant-select-selector) {
      background: var(--color-background);
      border-color: var(--color-border);
      color: var(--color-text);
    }

    :deep(.ant-pagination-options .ant-select-arrow) {
      color: var(--color-text-muted);
    }

    :deep(.ant-pagination-total-text) {
      color: var(--color-text-muted);
    }

    :deep(.ant-table-pagination) {
      margin: 16px 0 0;
    }
  }

  .user-avatar {
    border: 2px solid var(--color-border);
  }

  .role-tag {
    border-radius: var(--radius-full);
    font-weight: 500;
    font-size: 12px;
    padding: 2px 10px;
  }

  .time-text {
    color: var(--color-text-secondary);
    font-size: 13px;
  }

  .delete-btn {
    font-weight: 500;
    font-size: 13px;
    color: var(--color-error);
    padding: 4px 8px;

    &:hover {
      color: var(--color-error);
      opacity: 0.8;
    }
  }
}

@media (max-width: 768px) {
  #userManagePage {
    .search-form {
      flex-direction: column;
      align-items: stretch;

      :deep(.ant-form-item) {
        width: 100%;
      }
    }

    .search-input {
      width: 100%;
    }
  }
}
</style>
