from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

from django.conf.urls.i18n import i18n_patterns

from journal_numerique.views import Home
from django.contrib.auth import views as auth_views

admin.site.site_title = "Groupe 5 FD&IA UVBF 2024/2025 'Journal Numerique'"
admin.site.site_header = "Groupe 5 FD&IA UVBF 2024/2025 'Journal Numerique'"
admin.site.index_title = "Groupe 5 FD&IA UVBF 2024/2025 'Journal Numerique'"


urlpatterns = [    
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', Home.as_view(), name="home"),
    # path('', include('Accounts.urls')),
    # path('', include('notebook.urls')),
    path('accounts/', include('Accounts.urls')),
    path('notes/', include('notebook.urls')),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path('password_reset_send/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
)

