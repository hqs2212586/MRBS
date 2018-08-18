from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from django.contrib import auth
from .models import *
import datetime
import json


def login(request):
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")

        user = auth.authenticate(username=user, password=pwd)
        if user:
            # 登录成功
            auth.login(request, user)   # 注册request.user，可以拿到登录用户对象所有信息
            redirect("/index/")

    return render(request, "login.html")


def index(request):
    # 取当前日期
    date = datetime.datetime.now().date()
    print(date)  # 2018-08-17
    # 取预约日期，没有指定取当前日期
    book_date = request.GET.get("book_date", date)
    print(book_date)  # 2018-08-17

    # 拿到预定表中的时段
    time_choices = Book.time_choices
    # 拿到所有的会议室
    room_list = Room.objects.all()
    # 拿到预定信息
    book_list = Book.objects.filter(date=book_date)

    # 构建标签
    htmls = ""
    for room in room_list:   # 有多少会议室生成多少行，
        # 每行仅生成了第一列。还有其他td标签需要添加，因此此处没有闭合tr
        htmls += "<tr><td>{}({})</td>".format(room.caption, room.num)

        for time_choice in time_choices:   # 有多少时段就生成多少列

            flag = False   # False代表没有预定，True代表已经预定
            for book in book_list:    # 循环确定单元格是否被预定
                if book.room.pk == room.pk and book.time_id == time_choice[0]:
                    # 符合条件说明当前时段会议室已经被预定
                    flag = True
                    break
            print(book)   # 这个book是预定信息
            if flag:
                # 已经被预定,添加class='active'
                if request.user.pk == book.user.pk:
                    # 当前登录人查看自己的预约信息
                    htmls += "<td class='active item' room_id={} time_id={}>{}</td>".format(room.pk, time_choice[0],
                                                                                       book.user.username)
                else:
                    # 非当前登录人自己的预约信息
                    htmls += "<td class='another_active item' room_id={} time_id={}>{}</td>".format(room.pk, time_choice[0],
                                                                                       book.user.username)
            else:
                # 没有预定
                htmls += "<td class='item' room_id={} time_id={}></td>".format(room.pk, time_choice[0])

        # 循环完成后闭合tr标签
        htmls += "</tr>"

    return render(request, "index.html", locals())


def book(request):
    print(request.POST)
    post_data = json.loads(request.POST.get("post_data"))  # {"ADD":{"1":["5"],"2":["5","6"]},"DEL":{"3":["9","10"]}}
    choose_date = request.POST.get("choose_date")

    res = {"state": True, "msg": None}
    try:
        # 添加预定
        # post_data["ADD"] : {"1":["5"],"2":["5","6"]}

        book_list = []
        for room_id, time_id_list in post_data["ADD"].items():

            for time_id in time_id_list:
                book_obj = Book(user=request.user, room_id=room_id, time_id=time_id, date=choose_date)
                book_list.append(book_obj)

        Book.objects.bulk_create(book_list)

        # 删除预定
        from django.db.models import Q
        # post_data["DEL"]: {"2":["2","3"]}

        remove_book = Q()
        for room_id, time_id_list in post_data["DEL"].items():
            temp = Q()
            for time_id in time_id_list:
                temp.children.append(("room_id", room_id))
                temp.children.append(("time_id", time_id))
                temp.children.append(("user_id", request.user.pk))
                temp.children.append(("date", choose_date))
                remove_book.add(temp, "OR")
        if remove_book:
            Book.objects.filter(remove_book).delete()

    except Exception as e:
        res["state"] = False
        res["msg"] = str(e)

    return HttpResponse(json.dumps(res))
