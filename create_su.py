import os
import django
from django.contrib.auth import get_user_model
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

# Obtener el modelo de usuario

User = get_user_model()
username = 'pfuentea'
email = 'admin@example.com'
password = 'pfuentea-roca'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created successfully.')
