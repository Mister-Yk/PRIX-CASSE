from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .utiles import panier_cookie, data_cookie
from decimal import Decimal
from django.core.paginator import Paginator



def shop(request, *args, **kwargs):
    """ Vue principale """
    data = data_cookie(request)
    nombre_article = data['nombre_article']
    p = Paginator(Produit.objects.all(), 20)
    page = request.GET.get('page')
    products = p.get_page(page)

    if request.method == 'GET':
        name = request.GET.get('recherche')
        if name:
            produits = Produit.objects.filter(name__icontains=name)


    context = {
        'nombre_article': nombre_article,
        'products':products
    }

    return render(request, 'shop/index.html', context)


def panier(request, *args, **kwargs):
    data = data_cookie(request)
    articles=data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context={
        'articles':articles,
        'commande':commande,
        'nombre_article':nombre_article
    }     
    return render(request, 'shop/panier.html', context)

def commande(request, *args, **kwargs):
    data = data_cookie(request)
    articles=data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context={
        'articles':articles,
        'commande':commande,
        'nombre_article':nombre_article
    }    
    return render(request, 'shop/commande.html', context)


@login_required()
def updateArticle(request, *args, **kwargs):
    data = json.loads(request.body)
    produit_id =data['produit_id']
    action = data['action']

    produit = Produit.objects.get(id=produit_id)

    client = request.user.client
    commande, created = Commande.objects.get_or_create(client=client, complete=False)
    commande_article, created = CommandeArticle.objects.get_or_create(commande=commande, produit=produit)

    if action =='add':
        commande_article.quantite += 1

    if action=='remove':
        commande_article.quantite -=1
    commande_article.save()

    if commande_article.quantite <=0:
        commande_article.delete() 

    return JsonResponse("Panier modifier", safe=False)


def commandeAnonyme(request, data):
    name = data['form']['name']
    username = data['form']['username']
    email = data['form']['email']
    phone = data['form']['phone']
    cookie_panier = panier_cookie(request)
    articles = cookie_panier['articles']
    client, created = Client.objects.get_or_create(
        email = email
    )
    client.name = name
    client.username=username
    client.phone = phone
    client.save()
    commande = Commande.objects.create(
        client=client
    )
    for article in articles:
        produit = Produit.objects.get(id=article['produit']['pk'])
        CommandeArticle.objects.create(
            produit=produit,
            commande = commande,
            quantite = article['quantite']
        )
    return client, commande



def traitementCommande(request, *args, **kwargs):
    """ traitement,  validation de la com;ande  et verification de l'integrite des donnees(detection de fraude)"""

    STATUS_TRANSACTION = ['ACCEPTED', 'COMPLETED', 'SUCESS']
    
    transaction_id = datetime.now().timestamp()

    data = json.loads(request.body)

    print(data)

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)


    else:
        client, commande = commandeAnonyme(request, data)

    total = float(data['form']['total'])

    commande.transaction_id = data['payment_info']['transaction_id']

    commande.total_trans = total

    if commande.get_panier_total == total:

        commande.complete = True
        commande.status = data['payment_info']['status']

    else:
        commande.status = "REFUSED"
        commande.save()
        
        return JsonResponse("Attention!!! Traitement Refuse Fraude detecte!", safe=False)

    commande.save()    
    
    if not commande.status in STATUS_TRANSACTION:
        return JsonResponse("Désolé, le paiement a échoué, veuillez réessayer")    

  

    if commande.produit_physique:

        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse = data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )



    return JsonResponse("Votre paiement a été effectué avec succès, vous recevrez votre commande dans un instant !", safe=False)

def recherche(request):
    pass