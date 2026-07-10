<template>
  <div id="demoPage">
    <div class="page-header">
      <h1 class="page-title">组件测试</h1>
      <p class="page-subtitle">项目中自定义组件的展示与测试</p>
    </div>

    <div class="container">
      <!-- Logo -->
      <section class="demo-section">
        <h2 class="section-title">Logo</h2>
        <ApiTable :rows="logoApi" />
        <DemoBlock :code="logoCode">
          <div style="display: flex; gap: 40px; align-items: center">
            <Logo size="sm" />
            <Logo size="md" />
            <Logo size="lg" />
          </div>
        </DemoBlock>
      </section>

      <!-- Button -->
      <section class="demo-section">
        <h2 class="section-title">Button</h2>
        <ApiTable :rows="buttonApi" />
        <h3 class="sub-title">变体与大小</h3>
        <DemoBlock :code="buttonVariantsCode">
          <div style="display: flex; gap: 16px; align-items: center">
            <Button variant="primary" size="sm">小按钮</Button>
            <Button variant="primary" size="md">中按钮</Button>
            <Button variant="primary" size="lg">大按钮</Button>
            <Button variant="secondary" size="md">次要按钮</Button>
            <Button variant="gradient" size="md">搜索</Button>
          </div>
        </DemoBlock>

        <h3 class="sub-title">Block & Disabled</h3>
        <DemoBlock :code="buttonStateCode">
          <div style="display: flex; flex-direction: column; gap: 12px; width: 100%">
            <Button variant="primary" size="md" block>撑满宽度</Button>
            <Button variant="primary" size="md" disabled>禁用状态</Button>
          </div>
        </DemoBlock>

        <h3 class="sub-title">RouterLink</h3>
        <DemoBlock :code="buttonLinkCode">
          <Button to="/" size="md">跳转首页</Button>
        </DemoBlock>
      </section>

      <!-- Input -->
      <section class="demo-section">
        <h2 class="section-title">Input</h2>
        <ApiTable :rows="inputApi" />
        <DemoBlock :code="inputCode">
          <div style="display: flex; gap: 16px">
            <div style="width: 260px">
              <Input v-model:value="inputText" placeholder="请输入文本" size="large">
                <template #prefix>
                  <UserOutlined class="input-icon" />
                </template>
              </Input>
            </div>
            <div style="width: 260px">
              <Input
                v-model:value="inputPassword"
                placeholder="请输入密码"
                is-password
              >
                <template #prefix>
                  <LockOutlined class="input-icon" />
                </template>
              </Input>
            </div>
          </div>
        </DemoBlock>
      </section>

      <!-- Toast -->
      <section class="demo-section">
        <h2 class="section-title">Toast</h2>
        <ApiTable :rows="toastApi" />
        <DemoBlock :code="toastCode">
          <div style="display: flex; gap: 12px">
            <Button variant="primary" size="md" @click="toast.success('操作成功')">
              成功提示
            </Button>
            <Button variant="secondary" size="md" @click="toast.error('操作失败，请重试')">
              错误提示
            </Button>
            <Button variant="secondary" size="md" @click="toast.warning('请注意检查输入')">
              警告提示
            </Button>
            <Button variant="secondary" size="md" @click="toast.info('这是一条消息通知')">
              信息提示
            </Button>
          </div>
        </DemoBlock>
      </section>

      <!-- Message -->
      <section class="demo-section">
        <h2 class="section-title">Message</h2>
        <ApiTable :rows="messageApi" />
        <DemoBlock :code="messageCode">
          <div style="display: flex; gap: 12px">
            <Button variant="primary" size="md" @click="msg.success('操作成功')">
              成功消息
            </Button>
            <Button variant="secondary" size="md" @click="msg.error('操作失败，请重试')">
              错误消息
            </Button>
            <Button variant="secondary" size="md" @click="msg.warning('请注意检查输入')">
              警告消息
            </Button>
            <Button variant="secondary" size="md" @click="msg.info('这是一条消息通知')">
              信息消息
            </Button>
          </div>
        </DemoBlock>
      </section>

      <!-- EditorMockup -->
      <section class="demo-section">
        <h2 class="section-title">EditorMockup</h2>
        <DemoBlock :code="editorMockupCode">
          <EditorMockup />
        </DemoBlock>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { UserOutlined, LockOutlined } from "@ant-design/icons-vue";
import Logo from "@/components/Logo.vue";
import Button from "@/components/Button.vue";
import Input from "@/components/Input.vue";
import EditorMockup from "@/components/EditorMockup.vue";
import DemoBlock from "@/components/DemoBlock.vue";
import ApiTable from "@/components/ApiTable.vue";
import { useToast } from "@/composables/useToast";
import { useMessage } from "@/composables/useMessage";

const toast = useToast();
const msg = useMessage();
const inputText = ref("");
const inputPassword = ref("");

const logoApi = [
  { name: "size", desc: "Logo 尺寸", type: "'sm' | 'md' | 'lg'", default: "'sm'" },
];

const buttonApi = [
  { name: "variant", desc: "按钮变体：白底黑字 / 透明底白字 / 渐变蓝底", type: "'primary' | 'secondary' | 'gradient'", default: "'primary'" },
  { name: "size", desc: "按钮大小", type: "'sm' | 'md' | 'lg'", default: "'md'" },
  { name: "nativeType", desc: "原生 button 的 type 属性", type: "'button' | 'submit' | 'reset'", default: "'button'" },
  { name: "to", desc: "传入路径时渲染为 RouterLink", type: "string", default: "-" },
  { name: "disabled", desc: "是否禁用", type: "boolean", default: "false" },
  { name: "block", desc: "是否撑满容器宽度", type: "boolean", default: "false" },
];

const inputApi = [
  { name: "isPassword", desc: "是否为密码输入框", type: "boolean", default: "false" },
  { name: "size", desc: "输入框尺寸", type: "'large' | 'middle' | 'small'", default: "'large'" },
];

const toastApi = [
  { name: "success(msg, duration?)", desc: "成功提示", type: "function", default: "duration: 3000" },
  { name: "error(msg, duration?)", desc: "错误提示", type: "function", default: "duration: 3000" },
  { name: "warning(msg, duration?)", desc: "警告提示", type: "function", default: "duration: 3000" },
  { name: "info(msg, duration?)", desc: "信息提示", type: "function", default: "duration: 3000" },
];

const logoCode = `<Logo size="sm" />
<Logo size="md" />
<Logo size="lg" />`;

const buttonVariantsCode = `<Button variant="primary" size="sm">小按钮</Button>
<Button variant="primary" size="md">中按钮</Button>
<Button variant="primary" size="lg">大按钮</Button>
<Button variant="secondary" size="md">次要按钮</Button>
<Button variant="gradient" size="md">搜索</Button>`;

const buttonStateCode = `<Button variant="primary" size="md" block>撑满宽度</Button>
<Button variant="primary" size="md" disabled>禁用状态</Button>`;

const buttonLinkCode = `<Button to="/" size="md">跳转首页</Button>`;

const inputCode = `<Input v-model:value="text" placeholder="请输入文本" size="large">
  <template #prefix>
    <UserOutlined />
  </template>
</Input>

<Input v-model:value="password" placeholder="请输入密码" is-password>
  <template #prefix>
    <LockOutlined />
  </template>
</Input>`;

const toastCode = `import { useToast } from "@/composables/useToast";

const toast = useToast();

toast.success("操作成功");
toast.error("操作失败，请重试");
toast.warning("请注意检查输入");
toast.info("这是一条消息通知");`;

const messageApi = [
  { name: "success(msg, duration?)", desc: "成功消息", type: "function", default: "duration: 3000" },
  { name: "error(msg, duration?)", desc: "错误消息", type: "function", default: "duration: 3000" },
  { name: "warning(msg, duration?)", desc: "警告消息", type: "function", default: "duration: 3000" },
  { name: "info(msg, duration?)", desc: "信息消息", type: "function", default: "duration: 3000" },
];

const messageCode = `import { useMessage } from "@/composables/useMessage";

const msg = useMessage();

msg.success("操作成功");
msg.error("操作失败，请重试");
msg.warning("请注意检查输入");
msg.info("这是一条消息通知");`;

const editorMockupCode = `<EditorMockup />`;
</script>

<style scoped lang="scss">
#demoPage {
  min-height: 100vh;
  background: var(--color-background-secondary);
  padding-bottom: 80px;
}

.page-header {
  background: var(--gradient-hero);
  padding: 40px 20px;
  text-align: center;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 8px;
}

.page-subtitle {
  font-size: 14px;
  color: var(--color-text-secondary);
  margin: 0;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.demo-section {
  margin-top: 40px;

  .section-title {
    font-size: 22px;
    font-weight: 700;
    color: var(--color-text);
    margin: 0 0 8px;
  }

  .sub-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--color-text-secondary);
    margin: 24px 0 16px;
  }
}

.input-icon {
  color: var(--color-text-muted);
  font-size: 15px;
}
</style>
