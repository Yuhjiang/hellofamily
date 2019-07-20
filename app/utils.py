"""
增加常用模块
"""
import pymongo
from math import ceil
from flask import abort


def paginate(data, page=None, per_page=None, member_num=None):
    """
    实现分页
    :param: data: 查询到的数据
    :param page: 当前页面
    :param per_page: 每一页数据数量
    :param member_num: 检索图里的成员数
    :return:
    """

    items = data.limit(per_page).skip((page - 1) * per_page)
    items = list(items)

    if member_num:
        items = list(filter(lambda img: len(img['members']) == 2, list(items)))

    if page < 1:
        page = 1

    total = len(items)

    return Pagination(data, page, per_page, total, items)


class Pagination(object):
    def __init__(self, data, page, per_page, total, items):
        self.data = data
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        if self.page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self):
        return paginate(self.data, self.page - 1, self.per_page)

    @property
    def prev_num(self):
        if not self.has_prev():
            return None
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    def next(self):
        return paginate(self.data, self.page + 1, self.per_page)

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (self.page - left_current - 1 < num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
