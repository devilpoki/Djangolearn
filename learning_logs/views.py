from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required   # 使用login_required限制存取(當做裝飾器)

from .models import Topic, Entry
from .forms import TopicForm, EntryForm
# Create your views here.

def index(request):
    """The home page for Learning Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics."""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')    #限制只能存取屬於自已的主題
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

# 個別主題的view
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:         # 保護使用者主題edit_entry頁面
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html',context)

# 使用者輸入資料
@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit= False)    # 把新主題關聯到目前使用者
            new_topic.owner = request.user          # 把新主題關聯到目前使用者
            new_topic.save()                        # 把新主題關聯到目前使用者
            # form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

# new_entry 視圖函式
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return  render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))

    # 關鍵：這兩行必須在最外層（與 if/else 同等級），確保表單驗證不通過或 GET 請求時都能回傳頁面
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

