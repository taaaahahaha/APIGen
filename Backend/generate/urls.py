from django.urls import path
from . import views
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='APIs Available')


urlpatterns=[
    path('',views.index,name='index'),
    path('docs/', schema_view),
    # path('upload/', views.upload, name='upload'),
    # path('uploadfile/', views.uploadfile, name='uploadfile'),
    # path('run/', views.run, name='run'),
    # path('api/v1/stats/', views.stats, name='stats'),
    path('api/v1/stats/', views.stats, name='stats'),
    path('api/v1/<str:database>/<str:table>/freq/', views.frequent_query, name='frequent query'),
    path('api/v1/<str:database>/<str:table>/', views.dynamic_access, name='AutoGenerated'),
    path('api/v1/<str:database>/<str:table>/<str:id>/', views.dynamic_access, name='AutoGenerated'),
]