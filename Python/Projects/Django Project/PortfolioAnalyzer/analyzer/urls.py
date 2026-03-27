from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('analyze/', views.analyze_user, name='analyze'),
    path('result/<uuid:report_id>/', views.analysis_result, name='analysis_result'),
    path('history/', views.history, name='history'),
    path('compare/', views.compare_users, name='compare'),
    path('delete/<int:report_id>/', views.delete_report, name='delete_report'),
    path('share/<int:report_id>/', views.share_report, name='share_report'),
    path('analyze-repo/', views.analyze_repo_view, name='analyze_repo'),
]
