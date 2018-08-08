from django.urls import path

# This is a relative import - "from . import views" means
# "import views from the same directory as this file"
# An absolute import would be "from cogaware.distortions import views"
from . import views


urlpatterns = [
    # When you have an empty path, i.e. '/',
    # call the index function from views.py
    path('', views.index, name='index'),
    path('<int:trap_id>', views.trap, name='trap')
]
