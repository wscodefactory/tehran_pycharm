from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect
from .forms import NoticeForm
from .models import Notice
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

def notice_list(request):
    category = request.GET.get('category', '')
    query = request.GET.get('query', '')

    notices = Notice.objects.all().order_by('-id')

    if category:
        notices = notices.filter(category=category)

    if query:
        notices = notices.filter(title__icontains=query)

    paginator = Paginator(notices, 10)  # 페이지당 공지사항 개수
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'notice.html', {'page_obj': page_obj})



def create_notice_page(request):
    return render(request, 'create_notice.html')

def notice_detail(request, id):
    notice = get_object_or_404(Notice, pk=id)

    notice.viewcnt += 1
    notice.save()

    return render(request, 'notice_detail.html', {'notice': notice})

def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return redirect('/notice/notice') 
    else:
        form = NoticeForm()
    
    return render(request, 'create_notice.html', {'form': form})

def notice_update(request, id):
    notice = get_object_or_404(Notice, id=id)

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_detail', id=notice.id)
    else:
        form = NoticeForm(instance=notice)

    return render(request, 'notice_update.html', {'form': form, 'notice': notice})

def notice_delete(request, id):
    notice = get_object_or_404(Notice, id=id)

    if request.user.is_superuser:
        # 삭제 동작 처리
        notice.delete()
        return redirect('/notice/notice') 

    # 권한이 없는 경우, 혹은 POST 요청이 아닌 경우, 에러 처리
    return render(request, 'error.html', {'error_message': '삭제 권한이 없습니다.'})
    
