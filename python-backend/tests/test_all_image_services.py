"""测试所有 7 种配图方式"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.schemas.image import ImageRequest


def print_result(name: str, success: bool, detail: str = ""):
    icon = "✅" if success else "❌"
    print(f"  {icon} {name}: {detail}")


async def test_pexels():
    """测试 Pexels 图片搜索"""
    from app.services.pexels_service import PexelsService

    svc = PexelsService()
    try:
        url = await svc.search_image("nature landscape")
        await svc.close()
        if url and url.startswith("https://"):
            return True, f"搜索成功 -> {url[:80]}..."
        return False, f"返回异常: {url}"
    except Exception as e:
        return False, str(e)


async def test_nano_banana():
    """测试 Gemini 生图"""
    from app.services.nano_banana_service import NanoBananaService

    svc = NanoBananaService()
    try:
        result = await svc.generate_image_data(
            "A simple blue circle on white background, minimal style"
        )
        if result and result.is_valid():
            size = len(result.bytes) if result.bytes else 0
            return True, f"生成成功, size={size} bytes, mime={result.mime_type}"
        return False, "返回了空结果"
    except Exception as e:
        return False, str(e)


async def test_mermaid():
    """测试 Mermaid CLI"""
    from app.services.mermaid_service import MermaidService

    svc = MermaidService()
    if not svc.is_available():
        return False, "mmdc CLI 未安装"

    mermaid_code = """graph TD
    A[开始] --> B[结束]"""

    try:
        result = await svc.generate_diagram_data(mermaid_code)
        if result and result.is_valid():
            size = len(result.bytes) if result.bytes else 0
            return True, f"生成成功, size={size} bytes, format=svg"
        return False, "返回了空结果"
    except Exception as e:
        return False, str(e)


async def test_iconify():
    """测试 Iconify 图标搜索"""
    from app.services.iconify_service import IconifyService

    svc = IconifyService()
    try:
        url = await svc.search_image("home")
        await svc.close()
        if url and "api.iconify.design" in url:
            return True, f"搜索成功 -> {url[:80]}"
        return False, f"返回异常: {url}"
    except Exception as e:
        return False, str(e)


async def test_emoji_pack():
    """测试表情包搜索 (Bing 爬取)"""
    from app.services.emoji_pack_service import EmojiPackService

    svc = EmojiPackService()
    try:
        url = await svc.search_image("开心")
        await svc.close()
        if url and url.startswith("http"):
            return True, f"搜索成功 -> {url[:80]}..."
        return False, f"返回异常: {url}"
    except Exception as e:
        return False, str(e)


async def test_svg_diagram():
    """测试 SVG 示意图生成 (DeepSeek)"""
    from app.services.svg_diagram_service import SvgDiagramService

    svc = SvgDiagramService()
    request = ImageRequest(
        prompt="A simple bar chart showing sales data",
        keywords="bar chart",
    )
    try:
        result = await svc.get_image_data(request)
        if result and result.is_valid():
            size = len(result.bytes) if result.bytes else 0
            return True, f"生成成功, size={size} bytes"
        return False, "返回了空结果"
    except Exception as e:
        return False, str(e)


async def test_picsum():
    """测试 Picsum 兜底图片"""
    import httpx

    url = "https://picsum.photos/800/600?random=1"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, follow_redirects=True)
        if resp.status_code == 200 and len(resp.content) > 0:
            return True, f"获取成功, size={len(resp.content)} bytes, content-type={resp.headers.get('content-type', 'unknown')}"
        return False, f"HTTP {resp.status_code}"
    except Exception as e:
        return False, str(e)


async def main():
    print("=" * 55)
    print("测试所有配图方式")
    print("=" * 55)

    tests = [
        ("Pexels 图片搜索", test_pexels),
        ("Gemini 生图", test_nano_banana),
        ("Mermaid 流程图", test_mermaid),
        ("Iconify 图标", test_iconify),
        ("表情包搜索", test_emoji_pack),
        ("SVG 示意图", test_svg_diagram),
        ("Picsum 兜底", test_picsum),
    ]

    results = []
    for name, test_fn in tests:
        print(f"\n[{name}]")
        success, detail = await test_fn()
        print_result(name, success, detail)
        results.append((name, success))

    print("\n" + "=" * 55)
    print("汇总")
    print("=" * 55)
    ok = sum(1 for _, s in results if s)
    fail = len(results) - ok
    for name, success in results:
        icon = "✅" if success else "❌"
        print(f"  {icon} {name}")
    print(f"\n总计: {ok}/{len(results)} 可用, {fail} 不可用")


if __name__ == "__main__":
    asyncio.run(main())
