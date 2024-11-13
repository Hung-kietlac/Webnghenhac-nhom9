from pymongo import MongoClient
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import hashlib
import random

def home(request):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Nhac"]
    mycol = mydb["Nhac"]

    query = request.GET.get('q')
    if query:
        songs = list(mycol.find({
            "$or": [
                {"tenbaihat": {"$regex": query, "$options": "i"}},
                {"tencasi": {"$regex": query, "$options": "i"}}
            ]
        }))
    else:
        songs = list(mycol.find())
    
    random_songs = random.sample(songs, min(len(songs), 6))

    return render(request, 'app/home.html', {'songs': random_songs})

def dangky(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Nhac"]
    user_collection = db["User"]

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Mật khẩu không trùng khớp.")
            return render(request, 'app/dangky.html')

        if user_collection.find_one({"username": username}):
            messages.error(request, "Tên người dùng đã tồn tại.")
            return render(request, 'app/dangky.html')

        if user_collection.find_one({"email": email}):
            messages.error(request, "Email đã được đăng ký.")
            return render(request, 'app/dangky.html')

        hashed_password = make_password(password) #Mã hóa password

        user_data = {
            "email": email,
            "username": username,
            "password": hashed_password
        }
        user_collection.insert_one(user_data)

        messages.success(request, "Bạn đã đăng ký thành công!")
        return redirect('home')

    return render(request, 'app/dangky.html')

def dangnhap(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Nhac"]
    user_collection = db["User"]

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me', False)

        user = user_collection.find_one({"username": username})
        
        if user and check_password(password, user["password"]):
            # Nếu chọn "Nhớ mật khẩu" thì lưu vào cookie
            response = redirect('home')
            if remember_me:
                response.set_cookie('username', username, max_age=30*24*60*60)
                hashed_password = hashlib.sha256(password.encode()).hexdigest() #Giải mã password
                response.set_cookie('password', hashed_password, max_age=30*24*60*60)
            messages.success(request, "Bạn đã đăng nhập thành công!")
            return response
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
            return render(request, 'app/dangnhap.html')

    # Kiểm tra cookie để điền sẵn vào form đăng nhập
    username = request.COOKIES.get('username', '')
    password = request.COOKIES.get('password', '')

    return render(request, 'app/dangnhap.html', {'username': username, 'password': password})

def danhsachnhac(request):
    myclient = MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Nhac"]
    mycol = mydb["Nhac"]

    songs = list(mycol.find())

    return render(request, 'app/danhsachnhac.html', {'songs': songs})

def thuvien(request):
    return render(request, 'app/thuvien.html')