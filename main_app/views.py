# main_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Exists, OuterRef, Count, Subquery
from .forms import SignUpForm
from .models import Practice, Registration

def home(request):
    return render(request, 'main_app/home.html')

def practice_list(request):
    if request.user.is_authenticated:
        # ユーザーが登録しているRegistrationオブジェクトをSubqueryで取得
        registrations = Registration.objects.filter(user=request.user, practice=OuterRef('pk'))
        practices = Practice.objects.filter(is_closed=False).annotate(
            is_registered=Exists(registrations),
            registration_id=Subquery(registrations.values('id')[:1]),
            current_participants=Count('registration')
        )
    else:
        practices = Practice.objects.filter(is_closed=False).annotate(
            current_participants=Count('registration')
        )
    
    return render(request, 'main_app/practice_list.html', {'practices': practices})

@login_required
def register_practice(request, pk):
    practice = get_object_or_404(Practice, pk=pk)
    
    if practice.is_closed:
        messages.error(request, 'この練習の参加申請は締め切られています。')
        return redirect('main_app:practice_list')

    # 既に登録しているか確認
    if Registration.objects.filter(user=request.user, practice=practice).exists():
        messages.warning(request, 'すでにこの練習に参加登録しています。')
        return redirect('main_app:practice_list')

    # 定員に達しているか確認
    if practice.registration_set.count() >= practice.max_participants:
        messages.error(request, 'この練習は定員に達しています。')
        return redirect('main_app:practice_list')

    # 登録処理
    try:
        Registration.objects.create(user=request.user, practice=practice)
        messages.success(request, '参加登録が完了しました。')
    except IntegrityError:
        # 一意性制約に違反した場合（競合状態）
        messages.warning(request, 'すでにこの練習に参加登録しています。')

    return redirect('main_app:practice_list')

@login_required
def cancel_registration(request, pk):
    """
    ユーザーの参加登録をキャンセルするビュー
    """
    # Registrationオブジェクトを取得。ユーザーとregistration_idでフィルタリング
    registration = get_object_or_404(Registration, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # POSTリクエストであればキャンセル処理を実行
        registration.delete()
        messages.success(request, '参加登録をキャンセルしました。')
        return redirect('main_app:practice_list')
    
    # GETリクエストであれば確認ページを表示
    return render(request, 'main_app/cancel_registration.html', {'registration': registration})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ユーザーを自動的にログイン
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'アカウント「{username}」が作成され、ログインしました。')
            return redirect('main_app:home')  # ホームページにリダイレクト
        else:
            messages.error(request, '登録に失敗しました。正しい情報を入力してください。')
    else:
        form = SignUpForm()
    return render(request, 'main_app/signup.html', {'form': form})
