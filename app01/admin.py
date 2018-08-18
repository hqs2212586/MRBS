from django.contrib import admin

# Register your models here.
from app01.models import *


class BookConfig(admin.ModelAdmin):
    list_display = ["id", "user", "room", "date"]   # 不能放多对多字段
    list_display_links = ["room", "date"]   # 自由定制哪一列可以做跳转
    list_filter = ["user", "date"]   # 定制右侧快速筛选
    list_editable = ["user"]
    search_fields = ['date']
    date_hierarchy = 'date'

    # fields = ['user', ]
    exclude = ['user', 'room']

    # ordering = ["id"]
    ordering = ['-date', "time_id"]   # 反向排序

    # 定制Action行为具体方法
    def func(self, request, queryset):
        print(self, request, queryset)
        queryset.update(date="2012-12-12")

    func.short_description = "批量初始化操作"
    actions = [func, ]

    # Action选项都是在页面上方显示
    actions_on_top = True
    # Action选项都是在页面下方显示
    actions_on_bottom = False

    # 是否显示选择个数
    actions_selection_counter = True


admin.site.register(Book, BookConfig)
admin.site.register(UserInfo)
admin.site.register(Room)
