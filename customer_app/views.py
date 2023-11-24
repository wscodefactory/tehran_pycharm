from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.utils import timezone

def qna_list(request):
    questions = Question.objects.all().order_by('-created_at')

    category = request.GET.get('category', '')
    query = request.GET.get('query', '')

    if category:
        questions = questions.filter(category=category)

    if query:
        questions = questions.filter(title__icontains=query)

    paginator = Paginator(questions, 10)  # 페이지당 공지사항 개수
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer.html', {'page_obj': page_obj})

def search_qna(request):
    query = request.GET.get('query', '')
    questions = Question.objects.filter(title__icontains=query).order_by('-created_at')

    paginator = Paginator(questions, 10)  # 페이지당 질문 개수
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'customer.html', {'page_obj': page_obj})


def create_qna_page(request):
    return render(request, 'create_qna.html')

def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('qna_list')
    else:
        form = QuestionForm()
    return render(request, 'create_qna.html', {'form': form})

from django.shortcuts import get_object_or_404

def qna_detail(request, id):
    question = get_object_or_404(Question, pk=id)

    # 답변이 여러 개인 경우, 적절한 조건으로 필터링하여 가져옵니다.
    answers = Answer.objects.filter(question=question)

    if question.is_answered and answers.exists():
        answer = answers.first()  # 필요에 따라 조건에 맞게 선택
    else:
        answer = "답변 대기중"

    return render(request, 'qna_detail.html', {'question': question, 'answer': answer})


def answer_add(request, id):
    question = get_object_or_404(Question, pk=id)

    try:
        answer = Answer.objects.get(question=question)
    except Answer.DoesNotExist:
        answer = None

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            content = form.cleaned_data['content']
            author = request.user

            question.is_answered = True
            question.save()
            answer = Answer(content=content, question=question, author=author)

            answer.save()
            return redirect('qna_detail', id=id)
    else:
        form = AnswerForm(instance=answer) if answer else AnswerForm()

    return render(request, 'qna_detail.html', {'form': form, 'question': question, 'answer': answer})

def answer_update(request, id):
    # 해당 질문에 대한 모든 답변을 가져옵니다.
    question = get_object_or_404(Question, pk=id)
    answers = Answer.objects.filter(question=question)

    # 해당 질문에 대한 답변 중 첫 번째 답변을 가져옵니다.
    answer = answers.first() if answers.exists() else None

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            # 폼에서 전달된 데이터를 저장합니다.
            answer = form.save(commit=False)
            answer.created_at = timezone.now()
            answer.save()
            return redirect('qna_detail', id=question.id)
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'qna_detail.html', {'form': form, 'answer': answer})


from django.contrib import messages
from django.contrib import messages

def answer_delete(request, id):
    answer = get_object_or_404(Answer, id=id)

    # 권한 확인 - 로그인한 사용자와 답변을 작성한 사용자가 동일한지 확인합니다.
    if request.user.is_authenticated and (request.user.is_superuser or request.user == answer.author):
        question = answer.question  # 해당 답변이 속한 질문 가져오기
        answer.delete()  # 답변 삭제

        # 해당 질문의 is_answered 값을 False로 변경하여 "답변 대기중" 상태로 변경합니다.
        question.is_answered = False
        question.save()

        messages.success(request, '답변이 삭제되었습니다.')
        return redirect('qna_detail', id=question.id)

    # 권한이 없는 경우 에러 메시지를 표시합니다.
    messages.error(request, '삭제 권한이 없습니다.')
    return redirect('error_page')  # 권한 없음 페이지로 리다이렉트하거나 다른 처리 방식을 선택할 수 있습니다..

def qna_delete(request, id):
    qna = get_object_or_404(Question, id=id)

    if request.user.is_superuser:
        # 삭제 동작 처리
        qna.delete()
        return redirect('/customer/customer')

    # 권한이 없는 경우, 혹은 POST 요청이 아닌 경우, 에러 처리
    return render(request, 'error.html', {'error_message': '삭제 권한이 없습니다.'})