from django.urls import path
from . import views

urlpatterns = [
    path('', views.endpoint),
    #path('siswa/<int:year>', views.siswa),
    #path('avg/<str:s_id>', views.average),
    #path('input/summary', views.input_summary),
    path('ringkasan', views.ringkasan),
    path('sekolah', views.sekolahParser),
    path('prediksi', views.prediksi),
    # path('inputprediksi', views.input_prediction),
]
