from django.shortcuts import render
from .models import Topic,Entry
from django.http import HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    t = 'a b c d'
    return render(request,'learning_log/index.html',locals())
@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    return render(request,'learning_log/topics.html',locals())
@login_required
def topic(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if not_topic(request,topic):
        return Http404
    entries = topic.entry_set.order_by('-date_added')

    return render(request,'learning_log/topic.html',locals())
@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner =request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_log:topics'))
    return render(request,'learning_log/new_topic.html',locals())
@login_required
def new_entry(request,topic_id):
    topic = Topic.objects.get(id=topic_id)
    if not_topic(request,topic):
        return Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_log:topic',args=[topic_id]))
    return render(request, 'learning_log/new_entry.html', locals())
@login_required
def edit_entry(request,entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if not_topic(request,topic):
        return Http404

    if request.method!='POST':
        form= EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_log:topic',args=[topic.id]))
    return render(request,'learning_log/edit_entry.html',locals())

def not_topic(request,topic):
    if request.user != topic.owner:
        return True