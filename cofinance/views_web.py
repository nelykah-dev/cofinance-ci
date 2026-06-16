from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests

BASE_URL = 'http://127.0.0.1:8000/api'

# ==============================================
# Fonction qui crée une session requests avec les cookies Django
# ==============================================
def get_requests_session(request):
    """Crée une session requests avec les cookies de la requête Django + CSRF."""
    session = requests.Session()
    # Copier tous les cookies de la requête Django vers la session requests
    for key, value in request.COOKIES.items():
        session.cookies.set(key, value)
    # Ajouter l'en-tête CSRF si le cookie est présent
    csrf_token = request.COOKIES.get('csrftoken')
    if csrf_token:
        session.headers.update({'X-CSRFToken': csrf_token})
    return session

# ==============================================
# Vues d'authentification
# ==============================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        else:
            error = "Nom d'utilisateur ou mot de passe incorrect."
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/login/')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        role = request.POST.get('role', 'client')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password != password2:
            error = "Les mots de passe ne correspondent pas."
        elif len(password) < 8:
            error = "Le mot de passe doit faire au moins 8 caractères."
        else:
            from accounts.models import User
            if User.objects.filter(username=username).exists():
                error = "Ce nom d'utilisateur existe déjà."
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role=role,
                    phone=phone or '',
                    address=address or '',
                )
                login(request, user)
                return redirect('/dashboard/')
    return render(request, 'register.html', {'error': error})

# ==============================================
# Dashboard (redirection selon le rôle)
# ==============================================

@login_required(login_url='/login/')
def dashboard_view(request):
    session = get_requests_session(request)
    
    if request.user.role == 'admin':
        r = session.get(f'{BASE_URL}/dashboard/')
        data = r.json() if r.status_code == 200 else {}
        return render(request, 'dashboard_admin.html', {'data': data, 'user': request.user})
    
    elif request.user.role == 'agent':
        r_credits = session.get(f'{BASE_URL}/credits/?statut=en_analyse')
        credits = r_credits.json() if r_credits.status_code == 200 else []
        r_notifs = session.get(f'{BASE_URL}/notifications/')
        notifications = r_notifs.json() if r_notifs.status_code == 200 else []
        return render(request, 'dashboard_agent.html', {
            'credits_en_attente': credits,
            'notifications': notifications,
            'user': request.user
        })
    
    else:  # client
        r_notifs = session.get(f'{BASE_URL}/notifications/')
        notifications = r_notifs.json() if r_notifs.status_code == 200 else []
        return render(request, 'dashboard_client.html', {
            'notifications': notifications,
            'user': request.user
        })

# ==============================================
# Crédits
# ==============================================

@login_required(login_url='/login/')
def credits_view(request):
    session = get_requests_session(request)
    message = None
    
    if request.method == 'POST':
        montant = request.POST.get('montant_demande')
        duree = request.POST.get('duree_mois')
        motif = request.POST.get('motif')
        if montant and duree and motif:
            payload = {
                'montant_demande': float(montant),
                'duree_mois': int(duree),
                'motif': motif,
            }
            r = session.post(f'{BASE_URL}/credits/', json=payload)
            if r.status_code == 201:
                message = {'type': 'success', 'text': 'Demande soumise avec succès !'}
            else:
                message = {'type': 'error', 'text': f"Erreur : {r.text}"}
        else:
            message = {'type': 'error', 'text': 'Veuillez remplir tous les champs.'}
    
    r = session.get(f'{BASE_URL}/credits/')
    credits = r.json() if r.status_code == 200 else []
    return render(request, 'credits.html', {'credits': credits, 'message': message})

# ==============================================
# Remboursements
# ==============================================

@login_required(login_url='/login/')
def remboursements_view(request):
    session = get_requests_session(request)
    message = None
    
    if request.method == 'POST':
        payload = {
            'credit': request.POST.get('credit_id'),
            'montant': request.POST.get('montant_paye'),
            'note': request.POST.get('note', ''),
        }
        r = session.post(f'{BASE_URL}/remboursements/paiements/', json=payload)
        if r.status_code == 201:
            message = {'type': 'success', 'text': 'Paiement enregistré avec succès !'}
        else:
            message = {'type': 'error', 'text': f"Erreur : {r.text}"}
    
    r = session.get(f'{BASE_URL}/remboursements/historique/')
    paiements = r.json() if r.status_code == 200 else []
    return render(request, 'remboursements.html', {'paiements': paiements, 'message': message})

# ==============================================
# Assurance
# ==============================================

@login_required(login_url='/login/')
def assurance_view(request):
    session = get_requests_session(request)
    message = None
    
    if request.method == 'POST':
        payload = {
            'produit': request.POST.get('produit'),
            'date_expiration': request.POST.get('date_expiration'),
        }
        r = session.post(f'{BASE_URL}/assurance/souscrire/', json=payload)
        if r.status_code == 201:
            message = {'type': 'success', 'text': 'Souscription effectuée avec succès !'}
        else:
            message = {'type': 'error', 'text': f"Erreur : {r.text}"}
    
    produits = session.get(f'{BASE_URL}/assurance/produits/')
    souscriptions = session.get(f'{BASE_URL}/assurance/mes-souscriptions/')
    return render(request, 'assurance.html', {
        'produits': produits.json() if produits.status_code == 200 else [],
        'souscriptions': souscriptions.json() if souscriptions.status_code == 200 else [],
        'message': message
    })

# ==============================================
# Notifications
# ==============================================

@login_required(login_url='/login/')
def notifications_view(request):
    session = get_requests_session(request)
    r = session.get(f'{BASE_URL}/notifications/')
    notifications = r.json() if r.status_code == 200 else []
    return render(request, 'notifications.html', {'notifications': notifications})