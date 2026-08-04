"""测试 Agent4 配图分析的耗时"""
import asyncio
import time
from app.services.article_agent_service import ArticleAgentService
from app.schemas.article import ArticleState, TitleResult

# 模拟一篇中等长度的文章（约 2000 字，接近真实 Agent3 输出）
SAMPLE_CONTENT = """
## 为什么你的自律总是失败？问题不在意志力

你是否曾经下定决心要改变自己？比如每天早上六点起床、坚持读书一小时、戒掉短视频、开始健身计划。结果呢？大部分人都倒在了第三天。

这不仅仅是你的问题。根据一项针对 5000 名职场人士的调查，87% 的人表示自己制定的自律计划在一个月内就失败了。真正的问题是：你把自律看得太简单了。

## 自律不是意志力的问题，而是系统的问题

很多人以为自律就是靠意志力硬撑。但实际上，意志力是一种会消耗的有限资源，就像肌肉一样会疲劳。心理学家 Roy Baumeister 提出了著名的"自我损耗理论"，他发现人类的自控力资源是有限的，每次使用都会消耗一部分。

你有没有发现，在忙碌了一整天之后，晚上最容易放纵自己？这就是因为你的意志力已经在白天被工作、会议、人际关系消耗殆尽了。

那么，真正自律的人是怎么做到的？他们不依赖意志力，而是依赖系统。

## 搭建你的自律系统：四个核心要素

### 1. 环境设计

如果你想少吃零食，最有效的方法不是每天告诫自己"不要吃"，而是**根本不要买零食放在家里**。这就是环境设计的力量。

研究表明，环境因素对行为的影响比我们想象的要大得多。在一个实验中，当巧克力从桌上移到两米外的柜子里时，办公室员工的巧克力摄入量减少了 60%。仅仅是增加了两米的距离。

你应该这样设计环境：
- 把健身服放在床头，早上起来第一眼就能看到
- 删除手机上的娱乐 App，减少诱惑源
- 把水杯放在显眼位置，让自己多喝水
- 书桌上只放和工作相关的物品

### 2. 习惯锚定

习惯锚定是 BJ Fogg 博士在《福格行为模型》中提出的概念。它的核心思想是：把你想建立的新习惯，叠加在一个你已经有的旧习惯之上。

比如说：
- 每天刷牙后立刻做个俯卧撑
- 倒完咖啡后马上写下今天的三个任务
- 下班回家脱掉外套后直接换上运动服

旧习惯就像一个触发器，新习惯跟在后面执行，形成行为链条。这样做的好处是，你不需要额外提醒自己——旧习惯本身就是提醒。

### 3. 反馈机制

自律难坚持的一个核心原因是**反馈太慢**。你连续跑步三天，照镜子完全看不出变化。你坚持吃健康餐一周，体重秤上的数字纹丝不动。没有即时的正向反馈，大脑就会开始质疑坚持的意义。

聪明的自律者会人为制造反馈：
- 使用打卡日历，每完成一天就画一个大大的红圈
- 在社群中分享每日进展，获得他人认可
- 设立里程碑奖励（坚持 30 天就买那双心仪已久的跑鞋）
- 用 App 追踪数据，看自己的进步曲线

### 4. 身份认同

这是最深层次的自律驱动力。当你不再是在"做某事"，而是"成为某种人"的时候，自律就变得自然而然了。

不要说"我在努力戒烟"，而要说"我不抽烟"。不要说"我在尝试运动"，而要说"我是一个爱运动的人"。语言的改变会影响你的自我认知，而自我认知决定了你的行为模式。

## 重新定义自律

自律不是和自己较劲，不是在每次想放弃的时候狠狠逼自己一把。自律的本质是：**设计一个让你不需要太费力就能做出正确选择的系统**。

当你搭建好了环境、锚定了习惯、建立了反馈、认定了身份，你就不需要每天和意志力搏斗了。自律会成为你生活中最自然的部分。
"""


async def main():
    service = ArticleAgentService()

    # 模拟 Agent4 的完整输入，参考 agent4_analyze_image_requirements
    state = ArticleState()
    state.task_id = "timing_test_001"
    state.title = TitleResult(
        mainTitle="为什么你的自律总是失败？问题不在意志力",
        subTitle="用系统思维重新定义自律，让坚持不再靠硬撑",
    )
    state.content = SAMPLE_CONTENT
    state.enabled_image_methods = None  # 所有方式都可用

    # 构建 prompt（和真实流程一致）
    available_methods = service._build_available_methods_description(None)
    method_usage_guide = service._build_method_usage_guide(None)

    input_chars = len(SAMPLE_CONTENT)
    print(f"文章长度: {input_chars} 字符")
    print(f"模型: {service.model}")
    print(f"开始调用 Agent4...\n")

    start = time.time()
    try:
        await service.agent4_analyze_image_requirements(state)
        elapsed = time.time() - start

        output_chars = len(state.content) if state.content else 0
        req_count = len(state.image_requirements) if state.image_requirements else 0

        print(f"✓ Agent4 完成")
        print(f"  耗时: {elapsed:.1f} 秒")
        print(f"  输出 contentWithPlaceholders 长度: {output_chars} 字符")
        print(f"  LLM 回显比例: {output_chars / input_chars:.0%} (输出/输入)")
        print(f"  配图需求数: {req_count}")
        for req in (state.image_requirements or []):
            print(f"    - position={req.position}, type={req.type}, source={req.image_source}, keywords={req.keywords[:40] if req.keywords else '-'}")

    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ Agent4 失败, 耗时: {elapsed:.1f} 秒")
        print(f"  错误: {e}")


if __name__ == "__main__":
    asyncio.run(main())
