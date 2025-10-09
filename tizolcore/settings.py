"""
Django settings for tizolcore project, configured for Render deployment.
"""

from pathlib import Path
import os
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =======================================================================
# 1. SÉCURITÉ ET ENVIRONNEMENT (PRODUCTION & DÉVELOPPEMENT)
# =======================================================================

# 1.1 SECRET_KEY: Clé secrète. DOIT être définie comme variable d'environnement sur Render.
SECRET_KEY = os.environ.get('SECRET_KEY')

# Si la clé n'est pas trouvée (en développement local), utilisez une clé de secours.
# Ceci est une mesure de sécurité : la clé réelle est dans l'environnement de Render.
if not SECRET_KEY:
    # Utilisez une clé locale (NON utilisée en production)
    SECRET_KEY = '412f07d5cdc345692bcea26a2533bab9' 

# 1.2 DEBUG: False en production (Render), True en développement local.
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    DEBUG = False
    # Autoriser l'URL de Render et potentiellement Netlify (pour éviter des problèmes de sous-domaines)
    ALLOWED_HOSTS = [
        RENDER_EXTERNAL_HOSTNAME, 
        '.onrender.com', 
        '.netlify.app'
    ]
else:
    DEBUG = True
    # Autoriser l'accès local et toutes les requêtes en développement (le '*' est pratique)
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '*'] 
    
# =======================================================================
# 2. APPLICATIONS INSTALLÉES
# =======================================================================

INSTALLED_APPS = [
    # Applications de base Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # Doit être avant les apps tierces si elles utilisent staticfiles
    'django.contrib.staticfiles', 

    # Apps tierces et locales
    'corsheaders', 
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
    'schools',
    'students',
    'academics',
    'communication',
]

# =======================================================================
# 3. MIDDLEWARES 
# =======================================================================

MIDDLEWARE = [
    # Middleware CORS doit être placé très haut, AVANT CommonMiddleware
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    
    # WhiteNoise pour les fichiers statiques en production (doit être après SecurityMiddleware)
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =======================================================================
# 4. CONFIGURATION CORS
# =======================================================================

# Configurez les domaines autorisés (votre frontend Netlify)
CORS_ALLOWED_ORIGINS = [
    # La première URL doit être récupérée de l'environnement si définie
    os.environ.get('NETLIFY_FRONTEND_URL', 'http://localhost:3000'), 

    # Ajout direct des URLs de production (Netlify)
    'https://tizolapp-ecole-v1.netlify.app',
    'https://tizolapp-parent-v1.netlify.app',
]

# Autoriser les cookies et les credentials (nécessaire pour la session/JWT/CSRF si vous les utilisez)
CORS_ALLOW_CREDENTIALS = True

# =======================================================================
# 5. BASE DE DONNÉES (POSTGRESQL - RENDER)
# =======================================================================

# Render expose l'URL de connexion PostgreSQL via la variable d'environnement DATABASE_URL.
if RENDER_EXTERNAL_HOSTNAME:
    # Utilise la variable DATABASE_URL fournie par Render (PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True
        )
    }
else:
    # Utilise SQLite pour le développement local
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
# =======================================================================
# 6. FICHIERS STATIQUES (WHITENOISE)
# =======================================================================

# URL utilisée par Django dans les templates
STATIC_URL = 'static/'

# Chemin où Django collectera les fichiers statiques de toutes les apps
# WhiteNoise sert les fichiers à partir de ce dossier
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise Configuration:
# Utiliser le stockage compressé et manifest pour WhiteNoise
# ATTENTION: WhiteNoise est géré dans MIDDLEWARE.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# =======================================================================
# 7. TEMPLATES ET URLS
# =======================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'tizolcore.urls'
WSGI_APPLICATION = 'tizolcore.wsgi.application'

# ... (Le reste de votre fichier : PASSWORD_VALIDATORS, etc., reste inchangé) ...

# =======================================================================
# 8. CONFIGURATION UTILISATEUR ET DRF
# =======================================================================

# Modèle d'utilisateur personnalisé
# Vérifiez si 'schools.SchoolUser' est le modèle que vous souhaitez utiliser.
AUTH_USER_MODEL = 'schools.SchoolUser' 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}