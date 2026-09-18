"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    # Home page 首頁
    path('', views.index, name='index'),

    # Page that shows all topics. 顯示所有主題
    path('topics/', views.topics, name='topics'),

    # 顯示特定主題的詳細內容及條目 (Entry)
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # 使用者輸入資料 new_topic
    path('new_topic/', views.new_topic, name='new_topic'),

    # new_entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),

    # 編輯既有條目 (edit_entry)
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),

]
