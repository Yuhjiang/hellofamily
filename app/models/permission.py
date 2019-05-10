"""
权限类
FOLLOW      1       关注
COMMENT     2       评论
WRITE       4       写文章
MODERATE    8       管理评论
ADMIN       16      管理员
"""


class Permission(object):
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16
