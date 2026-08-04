-- 热门选题新增爆款指数、写作难度、平台适配字段
USE `mo-wen`;

ALTER TABLE hot_topic
    ADD COLUMN viralScore SMALLINT DEFAULT 5 NOT NULL COMMENT '爆款潜力指数 1-10',
    ADD COLUMN difficulty SMALLINT DEFAULT 3 NOT NULL COMMENT '写作难度 1-5，1=简单 5=困难',
    ADD COLUMN platforms VARCHAR(200) DEFAULT '' NOT NULL COMMENT '适配平台，逗号分隔';
