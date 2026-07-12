import asyncio
from openai import AsyncOpenAI
from app.config import settings


async def test_chat():
    client = AsyncOpenAI(
        api_key=settings.dashscope_api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 非流式调用
    response = await client.chat.completions.create(
        model=settings.dashscope_model,
        messages=[{"role": "user", "content": "你好，请介绍一下你自己"}],
    )
    print("=== 非流式调用 ===")
    print(response.choices[0].message.content)
    print()

    # 流式调用
    print("=== 流式调用 ===")
    stream = await client.chat.completions.create(
        model=settings.dashscope_model,
        messages=[{"role": "user", "content": "用一句话介绍 FastAPI"}],
        stream=True,
    )
    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(test_chat())
