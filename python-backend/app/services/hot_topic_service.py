"""热门选题服务"""

import asyncio
import json
import logging
from datetime import datetime

from openai import AsyncOpenAI

from app.config import settings
from app.constants.prompt import PromptConstant
from app.database import database

logger = logging.getLogger(__name__)


class HotTopicService:
    """热门选题服务"""

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.dashscope_api_key,
            base_url=settings.dashscope_base_url,
        )
        self.model = settings.dashscope_model

    async def generate_topics(self, year: int, month: int) -> list[dict]:
        """
        AI 生成热门选题并写入数据库

        Args:
            year: 目标年份
            month: 目标月份

        Returns:
            生成的选题列表
        """
        prompt = PromptConstant.HOT_TOPIC_PROMPT.format(year=str(year), month=str(month))

        logger.info(f"开始生成 {year}年{month}月 热门选题, model={self.model}")

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content or ""

        topics = self._parse_json_list_response(content)

        if not topics:
            raise ValueError("AI 生成热门选题为空或解析失败")

        # upsert 写入数据库：删除当月旧数据，插入新数据
        await self._upsert_topics(year, month, topics)

        logger.info(f"热门选题写入成功, 共 {len(topics)} 条")
        return topics

    async def get_hot_topics(self, year: int, month: int) -> list[dict]:
        """获取当前月份热门选题"""
        rows = await database.fetch_all(
            query="""
                SELECT id, topicText, emoji, viralScore, difficulty, platforms, updateTime
                FROM hot_topic
                WHERE year = :year AND month = :month AND isActive = 1 AND isDelete = 0
                ORDER BY sortOrder ASC, id ASC
            """,
            values={"year": year, "month": month},
        )
        return [dict(row) for row in rows]

    async def _upsert_topics(self, year: int, month: int, topics: list[dict]):
        """覆盖写入当月选题"""
        async with database.transaction():
            # 删除当月旧 AI 数据
            await database.execute(
                query="""
                    DELETE FROM hot_topic
                    WHERE year = :year AND month = :month AND source = 'AI'
                """,
                values={"year": year, "month": month},
            )
            # 插入新数据
            for i, item in enumerate(topics):
                await database.execute(
                    query="""
                        INSERT INTO hot_topic (topicText, emoji, year, month, source, viralScore, difficulty, platforms, sortOrder)
                        VALUES (:topicText, :emoji, :year, :month, 'AI', :viralScore, :difficulty, :platforms, :sortOrder)
                    """,
                    values={
                        "topicText": item.get("topicText", ""),
                        "emoji": item.get("emoji", "🔥"),
                        "viralScore": item.get("viralScore", 5),
                        "difficulty": item.get("difficulty", 3),
                        "platforms": item.get("platforms", ""),
                        "year": year,
                        "month": month,
                        "sortOrder": i,
                    },
                )

    @staticmethod
    def _parse_json_list_response(content: str) -> list[dict]:
        """解析 AI 返回的 JSON 数组"""
        content = content.strip()
        # 尝试去掉 markdown 代码块
        if content.startswith("```"):
            lines = content.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines)
        try:
            result = json.loads(content)
            if isinstance(result, list):
                return result
            if isinstance(result, dict) and "topics" in result:
                return result["topics"]
            return []
        except json.JSONDecodeError:
            logger.error(f"热门选题 JSON 解析失败, content={content[:500]}")
            return []

    async def start_scheduler(self):
        """后台定时刷新热门选题"""
        logger.info("热门选题定时任务启动")
        while True:
            try:
                now = datetime.now()
                await self.generate_topics(now.year, now.month)
                logger.info("热门选题生成成功, 24 小时后刷新")
                await asyncio.sleep(86400)
            except Exception:
                logger.exception("热门选题生成失败, 1 小时后重试")
                await asyncio.sleep(3600)
