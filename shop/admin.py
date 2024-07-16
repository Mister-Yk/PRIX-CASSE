from django.contrib import admin
from .models import*

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    list_filter= ('name',)
    search_fields = ('name',)
    list_per_page = (4)
    ordering = ['name']

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'price', 'image', 'date_ajout','categorie')
    list_filter = ('name', 'date_ajout')
    search_fields = ('name',)
    list_per_page = (4)
    ordering = ['name']
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name', 'description')
    list_filter=('name',)
    search_fields = ('name',)
    list_per_page = (4)
    ordering = ['name']
    


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display =('date_commande','client',  'complete', 'transaction_id','status', 'total_trans',)
    list_filter=('date_commande',)
    search_fields = ('date_commande',)
    list_per_page = (4)
    ordering = ['status']

@admin.register(CommandeArticle)
class CommandeArticleAdmin(admin.ModelAdmin):
    list_display = ('produit', 'quantite', 'date_added',)
    list_filter=('date_added',)
    search_fields = ('commande',)
    list_per_page = (4)
    ordering = ['date_added']

@admin.register(AddressChipping)
class AddressChippingAdmin(admin.ModelAdmin):
    list_display = ('date_ajout', 'client','commande','addresse','ville', 'zipcode',)
    list_filter=('date_ajout','client',)
    search_fields = ('client',)
    list_per_page = (4)
    ordering = ['date_ajout']