from django.urls import path,include
from .views import (index)

urlpatterns = [
    path("",index),
    # path('criminal/',include("criminal.urls")),
    # path('case/',include("cases.urls")),

]