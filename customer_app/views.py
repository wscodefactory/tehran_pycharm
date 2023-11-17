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
    answer = get_object_or_404(Answer, question=id)

    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES, instance=answer)
        if form.is_valid():
            form.save(commit=False)
            answer.created_at = timezone.now()
            form.save()
            return redirect('qna_detail', id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'answer_update.html', {'form': form, 'answer': answer})

def answer_delete(request, id):
    # 답변을 가져올 때, question=id로 가져오는데, 답변은 하나의 질문에만 속합니다.
    # 그러므로 get_object_or_404(Answer, question=id) 대신 get_object_or_404(Answer, id=id)을 사용해야 합니다.
    answer = get_object_or_404(Answer, id=id)

    if request.user.is_authenticated:
        # 관리자는 언제나 삭제 권한을 가집니다.
        if request.user.is_superuser:
            answer.delete()
            # 해당 질문의 is_answered 값을 0으로 업데이트
            question = answer.question
            question.is_answered = 0
            question.save()
            return redirect('qna_detail', id=question.id)

        # 작성자인 경우에만 삭제 권한을 가집니다.
        elif request.user == answer.user:
            answer.delete()
            # 해당 질문의 is_answered 값을 0으로 업데이트
            question = answer.question
            question.is_answered = 0
            question.save()
            return redirect('qna_detail', id=question.id)

    return render(request, 'error.html', {'error_message': '삭제 권한이 없습니다.'})