from pydantic import BaseModel, Field


class AgentLogVO(BaseModel):
    """智能体执行日志视图对象"""

    id: int
    task_id: str = Field(..., alias="taskId")
    agent_name: str = Field(..., alias="agentName")
    start_time: str = Field(..., alias="startTime")
    end_time: str | None = Field(None, alias="endTime")
    duration_ms: int | None = Field(None, alias="durationMs")
    status: str
    error_message: str | None = Field(None, alias="errorMessage")
    prompt: str | None = None
    input_data: str | None = Field(None, alias="inputData")
    output_data: str | None = Field(None, alias="outputData")
    create_time: str = Field(..., alias="createTime")
    update_time: str = Field(..., alias="updateTime")

    class Config:
        populate_by_name = True


class AgentExecutionStatsVO(BaseModel):
    """任务执行统计"""

    task_id: str = Field(..., alias="taskId")
    total_duration_ms: int = Field(..., alias="totalDurationMs")
    agent_count: int = Field(..., alias="agentCount")
    agent_durations: dict[str, int] = Field(
        default_factory=dict, alias="agentDurations"
    )
    overall_status: str = Field(..., alias="overallStatus")
    logs: list[AgentLogVO] = Field(default_factory=list)

    class Config:
        populate_by_name = True


# ==================== 数据统计仪表盘 ====================


class StatisticsQueryRequest(BaseModel):
    """统计查询请求"""

    granularity: str = Field(
        default="daily", description="统计粒度: daily/weekly/monthly"
    )
    time_range: str = Field(
        default="30d", alias="timeRange", description="时间范围: 7d/30d/90d"
    )
    start_date: str | None = Field(
        None, alias="startDate", description="自定义开始日期 YYYY-MM-DD"
    )
    end_date: str | None = Field(
        None, alias="endDate", description="自定义结束日期 YYYY-MM-DD"
    )

    class Config:
        populate_by_name = True


class CreationTrendItem(BaseModel):
    """创作趋势项"""

    date: str
    count: int


class CreationTrendVO(BaseModel):
    """创作趋势"""

    items: list[CreationTrendItem] = Field(default_factory=list)


class AgentPerformanceItem(BaseModel):
    """智能体性能项"""

    agent_name: str = Field(..., alias="agentName")
    total_calls: int = Field(..., alias="totalCalls")
    success_rate: float = Field(..., alias="successRate")
    avg_duration_ms: float = Field(..., alias="avgDurationMs")
    min_duration_ms: float = Field(..., alias="minDurationMs")
    max_duration_ms: float = Field(..., alias="maxDurationMs")

    class Config:
        populate_by_name = True


class AgentPerformanceVO(BaseModel):
    """智能体性能"""

    items: list[AgentPerformanceItem] = Field(default_factory=list)


class UserTrendItem(BaseModel):
    """用户趋势项"""

    date: str
    new_users: int = Field(..., alias="newUsers")
    new_vip: int = Field(..., alias="newVip")

    class Config:
        populate_by_name = True


class UserAnalysisVO(BaseModel):
    """用户分析"""

    total_users: int = Field(..., alias="totalUsers")
    total_vip: int = Field(..., alias="totalVip")
    vip_conversion_rate: float = Field(..., alias="vipConversionRate")
    trends: list[UserTrendItem] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class QuotaUsageItem(BaseModel):
    """配额使用项"""

    user_id: int = Field(..., alias="userId")
    user_account: str = Field(..., alias="userAccount")
    user_name: str | None = Field(None, alias="userName")
    quota_consumed: int = Field(..., alias="quotaConsumed")
    total_articles: int = Field(..., alias="totalArticles")

    class Config:
        populate_by_name = True


class QuotaUsageVO(BaseModel):
    """配额使用"""

    total_quota_consumed: int = Field(..., alias="totalQuotaConsumed")
    items: list[QuotaUsageItem] = Field(default_factory=list)


class DashboardStatsVO(BaseModel):
    """仪表盘全量统计"""

    creation_trend: CreationTrendVO = Field(..., alias="creationTrend")
    agent_performance: AgentPerformanceVO = Field(..., alias="agentPerformance")
    user_analysis: UserAnalysisVO = Field(..., alias="userAnalysis")
    quota_usage: QuotaUsageVO = Field(..., alias="quotaUsage")

    class Config:
        populate_by_name = True
