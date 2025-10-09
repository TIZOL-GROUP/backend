"""
Django settings for tizolcore project, configured for Render deployment.
"""

from pathlib import Path
import os
import dj_database_url  # NOUVEAU: Pour la connexion à la base de données de Render

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------------------------
# SECTION SÉCURITÉ ET ENVIRONNEMENT (PRODUCTION)
# -----------------------------------------------------------------------

# 1. SECRET_KEY: TOUJOURS utiliser une variable d'environnement en production!
# Render permet de définir des variables d'environnement.
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-insecure-key-pour-developpement-seulement') # À changer!

# 2. DEBUG: Doit être False en production
# Render définit généralement la variable 'RENDER' ou 'ON_RENDER'
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

if RENDER_EXTERNAL_HOSTNAME:
    # Si nous sommes sur Render, désactiver le mode DEBUG
    DEBUG = False
    
    # Render met le hostname externe dans cette variable d'environnement
    ALLOWED_HOSTS = [RENDER_EXTERNAL_HOSTNAME, '.netlify.app']
else:
    # Pour le développement local
    DEBUG = True
    ALLOWED_HOSTS = ['*'] # Autoriser toutes les requêtes locales

# -----------------------------------------------------------------------
# SECTION CORS (POUR CONNECTER NETLIFY)
# -----------------------------------------------------------------------
# Nécessite 'django-cors-headers' (déjà installé ou à installer)

INSTALLED_APPS = [
    # Applications de base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # Doit être après les apps Django de base si vous utilisez WhiteNoise
    'django.contrib.staticfiles', 

    # Apps tierces et locales
    'corsheaders', # AJOUTÉ : Pour autoriser les requêtes de Netlify
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
    'schools',
    'students',
    'academics',
    'communication',
]

MIDDLEWARE = [
    # Middleware CORS doit être placé très haut, AVANT CommonMiddleware
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    
    # AJOUTÉ : WhiteNoise pour les fichiers statiques en production
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurez les domaines autorisés (votre frontend Netlify)
CORS_ALLOWED_ORIGINS = [
    # La première URL doit être récupérée si NETLIFY_FRONTEND_URL est défini
    os.environ.get('NETLIFY_FRONTEND_URL', 'http://localhost:3000'), 

    # Ajout direct des URLs de production si vous ne voulez pas passer par une seule variable Render
    'https://tizolapp-ecole-v1.netlify.app',
    'https://tizolapp-parent-v1.netlify.app',
]

# Autoriser les cookies et les credentials (nécessaire pour la session/JWT/CSRF si vous les utilisez)
CORS_ALLOW_CREDENTIALS = True


# -----------------------------------------------------------------------
# SECTION BASE DE DONNÉES (POSTGRESQL - RENDER)
# -----------------------------------------------------------------------

# Render expose l'URL de connexion PostgreSQL via la variable d'environnement DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        # Utilisez l'URL de connexion de Render si elle est définie
        default='sqlite:///db.sqlite3', 
        conn_max_age=600,
        conn_health_checks=True,
    )
}
# Ceci utilise la configuration PostgreSQL de Render si la variable DATABASE_URL est présente.
# Sinon, il utilise SQLite pour le développement local.

# -----------------------------------------------------------------------
# SECTION FICHIERS STATIQUES (WHITENOISE)
# -----------------------------------------------------------------------

# URL utilisée par Django dans les templates
STATIC_URL = 'static/'

# Chemin où Django collectera les fichiers statiques de toutes les apps
# WhiteNoise sert les fichiers à partir de ce dossier
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise Configuration:
# Utiliser le stockage compressé et manifest pour WhiteNoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # <-- VÉRIFIEZ CETTE LIGNE
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

# -----------------------------------------------------------------------
# AUTRES CONFIGURATIONS
# -----------------------------------------------------------------------

# ... (Le reste de votre fichier : TEMPLATES, PASSWORD_VALIDATORS, etc., reste inchangé) ...

ROOT_URLCONF = 'tizolcore.urls'
WSGI_APPLICATION = 'tizolcore.wsgi.application'

AUTH_USER_MODEL = 'schools.SchoolUser' # Utiliser SchoolUser si vous l'avez corrigé dans votre app 'schools'
# Si votre modèle personnalisé est dans l'app 'users', il doit être 'users.User'.
# J'ai remis 'schools.SchoolUser' pour éviter le conflit initial

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}