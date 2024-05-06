from django.urls import path, include
from shophubapp import views
from shophub import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('home', views.home),
    path('about', views.about),
    path('ps5', views.psconsole),
    path('xbox', views.xbxconsole),
    path('switch', views.swchconsole),
    path('psgames', views.psgames),
    path('xbxgames', views.xbxgames),
    path('pcgames', views.pcgames),
    path('nsgames', views.nsgames),
    path('login', views.user_login),
    path('register', views.register),
    path('cart', views.viewcart),
    path('logout', views.user_logout),
    path('condets/<cid>', views.condets),
    path('gamedets/<gid>', views.gamedets),
    path('range/', views.range),
    path('addtocart/console/<int:itid>', views.addtocart, {'itype': 'console'}, name = 'add_console_to_cart'),
    path('addtocart/game/<int:itid>', views.addtocart, {'itype': 'game'}, name = 'add_game_to_cart'),
    path('updateqty/<qv>/<cid>', views.updateqty, name = 'updateqty'),
    path('remove/<uid>/', views.remove, name = 'remove_item'),
    path('ordrconfo', views.ordrconfo),
    path('makepayment', views.makepayment),
    path('sendusermail', views.sendusermail),
    path('search', views.search),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)