"""数据统计服务"""

from datetime import datetime, timedelta

from databases import Database

from app.schemas.statistics import (
    AgentPerformanceItem,
    AgentPerformanceVO,
    CreationTrendItem,
    CreationTrendVO,
    DashboardStatsVO,
    QuotaUsageItem,
    QuotaUsageVO,
    StatisticsQueryRequest,
    UserAnalysisVO,
    UserTrendItem,
)


class StatisticsService:
    """数据统计服务"""

    def __init__(self, db: Database):
        self.db = db

    async def get_dashboard_stats(
        self, request: StatisticsQueryRequest
    ) -> DashboardStatsVO:
        """获取仪表盘全量统计数据"""
        start_date, end_date = self._resolve_date_range(request)

        creation_trend = await self._get_creation_trends(
            start_date, end_date, request.granularity
        )
        agent_perf = await self._get_agent_performance(start_date, end_date)
        user_analysis = await self._get_user_analysis(
            start_date, end_date, request.granularity
        )
        quota_usage = await self._get_quota_usage(start_date, end_date)

        return DashboardStatsVO(
            creationTrend=creation_trend,
            agentPerformance=agent_perf,
            userAnalysis=user_analysis,
            quotaUsage=quota_usage,
        )

    def _resolve_date_range(self, request: StatisticsQueryRequest):
        """解析日期范围"""
        if request.start_date and request.end_date:
            return request.start_date + " 00:00:00", request.end_date + " 23:59:59"

        days = {"7d": 7, "30d": 30, "90d": 90}.get(request.time_range, 30)
        end = datetime.now()
        start = end - timedelta(days=days)
        return start.strftime("%Y-%m-%d 00:00:00"), end.strftime("%Y-%m-%d 23:59:59")

    @staticmethod
    def _trunc_sql(granularity: str) -> str:
        """根据统计粒度返回 MySQL 日期截取表达式"""
        if granularity == "weekly":
            return "DATE_FORMAT(createTime, '%Y-%u')"
        elif granularity == "monthly":
            return "DATE_FORMAT(createTime, '%Y-%m')"
        return "DATE(createTime)"

    @staticmethod
    def _trunc_sql_alias(granularity: str) -> str:
        """日期截取 SELECT 列 + 别名"""
        trunc = StatisticsService._trunc_sql(granularity)
        return f"{trunc} AS date"

    async def _get_creation_trends(
        self, start_date: str, end_date: str, granularity: str
    ) -> CreationTrendVO:
        """文章创建趋势"""
        trunc_sql = self._trunc_sql(granularity)
        trunc_alias = self._trunc_sql_alias(granularity)

        rows = await self.db.fetch_all(
            query=f"""
                SELECT {trunc_alias}, COUNT(*) AS count
                FROM article
                WHERE isDelete = 0
                  AND createTime >= :start_date
                  AND createTime <= :end_date
                GROUP BY {trunc_sql}
                ORDER BY date ASC
            """,
            values={"start_date": start_date, "end_date": end_date},
        )

        items = [
            CreationTrendItem(date=str(row["date"]), count=row["count"]) for row in rows
        ]
        return CreationTrendVO(items=items)

    async def _get_agent_performance(
        self, start_date: str, end_date: str
    ) -> AgentPerformanceVO:
        """智能体执行性能统计"""
        rows = await self.db.fetch_all(
            query="""
                SELECT
                    agentName,
                    COUNT(*) AS totalCalls,
                    ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)
                          / COUNT(*) * 100, 2) AS successRate,
                    ROUND(AVG(durationMs), 2) AS avgDurationMs,
                    ROUND(MIN(durationMs), 2) AS minDurationMs,
                    ROUND(MAX(durationMs), 2) AS maxDurationMs
                FROM agent_log
                WHERE isDelete = 0
                  AND durationMs IS NOT NULL
                  AND createTime >= :start_date
                  AND createTime <= :end_date
                GROUP BY agentName
                ORDER BY totalCalls DESC
            """,
            values={"start_date": start_date, "end_date": end_date},
        )

        items = [
            AgentPerformanceItem(
                agentName=row["agentName"],
                totalCalls=row["totalCalls"],
                successRate=float(row["successRate"]),
                avgDurationMs=float(row["avgDurationMs"]),
                minDurationMs=float(row["minDurationMs"]),
                maxDurationMs=float(row["maxDurationMs"]),
            )
            for row in rows
        ]
        return AgentPerformanceVO(items=items)

    async def _get_user_analysis(
        self, start_date: str, end_date: str, granularity: str
    ) -> UserAnalysisVO:
        """用户分析：总数 + 趋势"""
        total_users = await self.db.fetch_val(
            query="SELECT COUNT(*) FROM user WHERE isDelete = 0 AND createTime <= :end_date",
            values={"end_date": end_date},
        )
        total_vip = await self.db.fetch_val(
            query="SELECT COUNT(*) FROM user WHERE isDelete = 0 AND userRole = 'vip'",
        )

        vip_rate = (
            round(float(total_vip) / float(total_users) * 100, 2)
            if total_users > 0
            else 0.0
        )

        # 注册趋势
        trunc_sql = self._trunc_sql(granularity)
        trunc_alias = self._trunc_sql_alias(granularity)

        reg_rows = await self.db.fetch_all(
            query=f"""
                SELECT {trunc_alias}, COUNT(*) AS newUsers
                FROM user
                WHERE isDelete = 0
                  AND createTime >= :start_date
                  AND createTime <= :end_date
                GROUP BY {trunc_sql}
                ORDER BY date ASC
            """,
            values={"start_date": start_date, "end_date": end_date},
        )

        # VIP 转化趋势
        vip_rows = await self.db.fetch_all(
            query=f"""
                SELECT {self._trunc_sql_alias(granularity)},
                       COUNT(DISTINCT userId) AS newVip
                FROM payment_record
                WHERE status = 'SUCCEEDED'
                  AND createTime >= :start_date
                  AND createTime <= :end_date
                GROUP BY {self._trunc_sql(granularity)}
                ORDER BY date ASC
            """,
            values={"start_date": start_date, "end_date": end_date},
        )

        vip_map: dict[str, int] = {str(r["date"]): r["newVip"] for r in vip_rows}
        trends = [
            UserTrendItem(
                date=str(r["date"]),
                newUsers=r["newUsers"],
                newVip=vip_map.get(str(r["date"]), 0),
            )
            for r in reg_rows
        ]

        return UserAnalysisVO(
            totalUsers=total_users,
            totalVip=total_vip,
            vipConversionRate=vip_rate,
            trends=trends,
        )

    async def _get_quota_usage(self, start_date: str, end_date: str) -> QuotaUsageVO:
        """配额使用情况"""
        total = await self.db.fetch_val(
            query="""
                SELECT COUNT(*) FROM article
                WHERE isDelete = 0
                  AND createTime >= :start_date
                  AND createTime <= :end_date
            """,
            values={"start_date": start_date, "end_date": end_date},
        )

        rows = await self.db.fetch_all(
            query="""
                SELECT
                    u.id AS userId,
                    u.userAccount,
                    u.userName,
                    COUNT(a.id) AS quotaConsumed,
                    COUNT(a.id) AS totalArticles
                FROM article a
                INNER JOIN user u ON a.userId = u.id AND u.isDelete = 0
                WHERE a.isDelete = 0
                  AND a.createTime >= :start_date
                  AND a.createTime <= :end_date
                GROUP BY u.id, u.userAccount, u.userName
                ORDER BY quotaConsumed DESC
                LIMIT 20
            """,
            values={"start_date": start_date, "end_date": end_date},
        )

        items = [
            QuotaUsageItem(
                userId=row["userId"],
                userAccount=row["userAccount"],
                userName=row["userName"],
                quotaConsumed=row["quotaConsumed"],
                totalArticles=row["totalArticles"],
            )
            for row in rows
        ]
        return QuotaUsageVO(totalQuotaConsumed=total, items=items)
