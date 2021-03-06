from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """用户信息表"""
    tel = models.CharField(max_length=32)


class Room(models.Model):
    """会议室表"""
    caption = models.CharField(max_length=32)   # 会议室名字
    num = models.IntegerField()   # 会议室容纳人数

    def __str__(self):
        return self.caption


class Book(models.Model):
    """会议室预订信息"""
    user = models.ForeignKey("UserInfo", on_delete=models.CASCADE)   # CASCADE级联删除
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    date = models.DateField()  # 日期
    time_choices = (    # 时段
        (1, '8:00'),
        (2, '9:00'),
        (3, '10:00'),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )
    time_id = models.IntegerField(choices=time_choices)    # 存数字，choices参数

    class Meta:
        unique_together = (   # 三个联合唯一，防止有人重复预定
            ('room', 'date', 'time_id'),
        )

    def __str__(self):
        return str(self.user) + "预定了" + str(self.room)