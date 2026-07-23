-- 为 user 表添加 VIP 过期时间字段，支持月付/年付会员
-- NULL 表示永久会员，有值表示到期自动降级
USE mo-wen;

ALTER TABLE user
    ADD COLUMN vipExpireTime DATETIME NULL COMMENT 'VIP过期时间，NULL=永久会员' AFTER vipTime;
