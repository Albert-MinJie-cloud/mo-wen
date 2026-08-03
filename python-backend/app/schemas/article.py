"""文章相关请求/响应模型"""

from typing import Any

from pydantic import BaseModel, Field

from app.schemas.common import PageRequest


class ArticleCreateRequest(BaseModel):
    """创建文章请求"""

    topic: str = Field(..., min_length=1, description="选题")
    style: str | None = Field(
        None, description="文章风格：tech/emotional/educational/humorous"
    )
    enabled_image_methods: list[str] | None = Field(
        None,
        alias="enabledImageMethods",
        description="允许的配图方式列表（为空表示支持所有方式）",
    )


class ArticleQueryRequest(PageRequest):
    """文章查询请求"""

    id: int | None = Field(None, description="文章 ID")
    task_id: str | None = Field(None, alias="taskId", description="任务 ID")
    user_id: int | None = Field(None, alias="userId", description="用户 ID")
    topic: str | None = Field(None, description="选题")
    status: str | None = Field(None, description="状态")


class TitleOption(BaseModel):
    """标题方案"""

    main_title: str = Field(..., alias="mainTitle")
    sub_title: str = Field(..., alias="subTitle")

    class Config:
        populate_by_name = True


class ArticleVO(BaseModel):
    """文章视图对象"""

    id: int
    task_id: str = Field(..., alias="taskId")
    user_id: int = Field(..., alias="userId")
    topic: str
    user_description: str | None = Field(None, alias="userDescription")
    style: str | None = None
    main_title: str | None = Field(None, alias="mainTitle")
    sub_title: str | None = Field(None, alias="subTitle")
    title_options: list[TitleOption] | None = Field(None, alias="titleOptions")
    outline: list[Any] | None = None
    content: str | None = None
    full_content: str | None = Field(None, alias="fullContent")
    cover_image: str | None = Field(None, alias="coverImage")
    images: list[Any] | None = None
    status: str
    phase: str | None = None
    error_message: str | None = Field(None, alias="errorMessage")
    create_time: str = Field(..., alias="createTime")
    completed_time: str | None = Field(None, alias="completedTime")
    update_time: str = Field(..., alias="updateTime")

    class Config:
        populate_by_name = True


# ArticleState 内部类定义
class TitleResult(BaseModel):
    """标题结果"""

    main_title: str = Field(..., alias="mainTitle")
    sub_title: str = Field(..., alias="subTitle")

    class Config:
        populate_by_name = True


class OutlineSection(BaseModel):
    """大纲章节"""

    section: int
    title: str
    points: list[str]


class OutlineResult(BaseModel):
    """大纲结果"""

    sections: list[OutlineSection]


class ImageRequirement(BaseModel):
    """配图需求"""

    position: int
    type: str
    section_title: str = Field(..., alias="sectionTitle")
    keywords: str
    image_source: str = Field(..., alias="imageSource", description="图片来源")
    prompt: str = Field(default="", description="AI 生图提示词")
    placeholder_id: str = Field(..., alias="placeholderId", description="占位符ID")

    class Config:
        populate_by_name = True


class ImageResult(BaseModel):
    """配图结果"""

    position: int
    url: str
    method: str
    keywords: str
    section_title: str = Field(..., alias="sectionTitle")
    description: str
    placeholder_id: str = Field(..., alias="placeholderId", description="占位符ID")

    class Config:
        populate_by_name = True


class Agent4Result(BaseModel):
    """智能体4返回结果（占位符方案）"""

    content_with_placeholders: str = Field(..., alias="contentWithPlaceholders")
    image_requirements: list[ImageRequirement] = Field(..., alias="imageRequirements")

    class Config:
        populate_by_name = True


class ArticleState:
    """文章生成状态（智能体间共享的状态对象）"""

    def __init__(self):
        self.task_id: str | None = None
        self.topic: str | None = None
        self.user_description: str | None = None
        self.style: str | None = None
        self.phase: str | None = None
        self.title_options: list[TitleOption] | None = None
        self.enabled_image_methods: list[str] | None = None
        self.title: TitleResult | None = None
        self.outline: OutlineResult | None = None
        self.content: str | None = None
        self.image_requirements: list[ImageRequirement] | None = None
        self.images: list[ImageResult] | None = None
        self.cover_image: str | None = None
        self.full_content: str | None = None


class ArticleConfirmTitleRequest(BaseModel):
    """确认标题请求"""

    task_id: str = Field(..., alias="taskId", min_length=1)
    selected_main_title: str = Field(..., alias="selectedMainTitle", min_length=1)
    selected_sub_title: str = Field(..., alias="selectedSubTitle", min_length=1)
    user_description: str | None = Field(None, alias="userDescription")

    class Config:
        populate_by_name = True


class ArticleConfirmOutlineRequest(BaseModel):
    """确认大纲请求"""

    task_id: str = Field(..., alias="taskId", min_length=1)
    outline: list[OutlineSection] = Field(..., min_length=1)

    class Config:
        populate_by_name = True


class ArticleAiModifyOutlineRequest(BaseModel):
    """AI 修改大纲请求"""

    task_id: str = Field(..., alias="taskId", min_length=1)
    modify_suggestion: str = Field(..., alias="modifySuggestion", min_length=1)

    class Config:
        populate_by_name = True
