from django.urls import path, include
from . import views

urlpatterns = [
    path('markdownx/', include('markdownx.urls')),
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('submit_solution/', views.submit_solution, name='submit_solution'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('logout/', views.logout_view, name='logout'),
    path('faq/', views.faq, name='faq'),
    path('rules/', views.rules, name='rules'),
    path('docs/', views.docs, name='docs'),
    path('api/download_solutions/', views.download_solutions, name='download_solutions'),
    path('api/upload_results/', views.upload_results, name='upload_results'),
]