from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from shophubapp.models import console, game, Cart, Order
import random 
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.contrib import messages
import uuid
import razorpay
from django.core.mail import send_mail

# Create your views here.

def index(request):
    return redirect('/home')

# Login Page
def user_login(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        # print(uname,":",upass)
        context = {}
        if uname == "" or upass == "":
            context['errmsg'] = "Fields cannot be empty"
            return render(request, 'login.html', context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:
                login(request,u)
                return redirect('/home')
            else:
                context['errmsg'] = "Invalid Username/Password"
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

# Register Page
def register(request):
    if request.method == "POST":
        uname = request.POST['uname']
        upass = request.POST['upass']
        ucpass = request.POST['ucpass']
        # print(uname, upass)
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context['errmsg'] = "Fields cannot be empty"
            return render(request, 'register.html', context)
        elif upass != ucpass:
            context['errmsg'] = "Password and Confirm Password do not match"
            return render(request, 'register.html', context)
        else:
            try:
                u = User.objects.create(password = upass, username = uname, email = uname)
                u.set_password(upass)
                u.save()
                context['success'] = "User Registered Successfully!! Please Login."
                return render(request, 'register.html', context)
            except Exception:
                context['errmsg'] = "Username already exists! Try another one."
                return render(request, 'register.html', context)
    else:
        return render(request, 'register.html')

# Logout Functionality
def user_logout(request):
    logout(request)
    return redirect('/login')

# Home Page
def home(request):
    userid = request.user.id
    uname = request.user.username
    print("Username: ",uname)
    print("UserID: ",userid)
    print("User Logged In? : ", request.user.is_authenticated)
    context = {}
    g = game.objects.filter(is_active=True)
    glist = list(g)
    tgame = random.sample(glist, min(len(glist),8))
    context['trgames'] = tgame
    return render(request, 'home.html', context)

# PS Console Page
def psconsole(request):
    context = {}
    c = console.objects.filter(is_active=True)
    context['consoles'] = c
    # print(c)
    return render(request, 'psconsole.html', context)

# Xbox Console Page
def xbxconsole(request):
    context = {}
    c = console.objects.filter(is_active=True)
    context['consoles'] = c
    # print(c)
    return render(request, 'xbxconsole.html', context)

# Switch Console Page
def swchconsole(request):
    context = {}
    c = console.objects.filter(is_active=True)
    context['consoles'] = c
    # print(c)
    return render(request, 'swchconsole.html', context)

# PS Games Page
def psgames(request):
    context = {}
    g = game.objects.filter(is_active=True, pltfrm=1)
    glist = list(g)
    tgame = random.sample(glist, min(len(glist),6))
    context['games'] = g
    context['trgames'] = tgame
    return render(request, 'psgames.html', context)

# Xbox Games Page
def xbxgames(request):
    context = {}
    g = game.objects.filter(is_active=True, pltfrm=2)
    glist = list(g)
    tgame = random.sample(glist, min(len(glist),6))
    context['games'] = g
    context['trgames'] = tgame
    return render(request, 'xbxgames.html', context)

# PC Games Page
def pcgames(request):
    context = {}
    g = game.objects.filter(is_active=True, pltfrm=4)
    glist = list(g)
    tgame = random.sample(glist, min(len(glist),6))
    context['games'] = g
    context['trgames'] = tgame
    return render(request, 'pcgames.html', context)

# Switch Games Page
def nsgames(request):
    context = {}
    g = game.objects.filter(is_active=True, pltfrm=3)
    glist = list(g)
    tgame = random.sample(glist, min(len(glist),6))
    context['games'] = g
    context['trgames'] = tgame
    return render(request, 'nsgames.html', context)

# Console Details Fucntion
def condets(request, cid):
    c = console.objects.filter(id = cid)
    context = {}
    context['consoles'] = c
    return render(request, 'prod_dets.html', context)

# Game Details Function
def gamedets(request, gid):
    g = game.objects.filter(id = gid)
    context = {}
    context['games'] = g
    return render(request, 'prod_dets.html', context)

# Add To Cart Function
def addtocart(request, itype, itid):
    if not request.user.is_authenticated:
        return redirect('/login')
    u = request.user
    context = {}

    if itype == 'console':
        i = get_object_or_404(console, id = itid)
        context['consoles'] = [i]
    elif itype == 'game':
        i = get_object_or_404(game, id = itid)
        context['games'] = [i]
    else:
        return HttpResponse("Invalid item type!")       #handle unexpected item type
    
    crt_itm = Cart.objects.filter(uid = u, itype = itype, itid = itid)
    
    if crt_itm.exists():
        messages.error(request, "Product Already Exists in Cart!!")
        return render(request, 'prod_dets.html', context)
    else:
        Cart.objects.create(uid = u, itype = itype, itid = itid)
        messages.success(request, 'Product Added To Cart Successfully!!')
        return render(request, 'prod_dets.html', context)


# Cart Page
def viewcart(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    citems = Cart.objects.filter(uid = request.user)
    # print('cart items: ', citems)
    
    if not citems:
        return render(request, 'emptycrt.html')

    fcrt = []
    s = 0
    for item in citems:
        if item.itype == 'console':
            ditem = get_object_or_404(console, id = item.itid)
            tot = ditem.price * item.qty
            s += tot
            print("price for item {} is {}".format(ditem.id, tot))
            fcrt.append({'item': ditem, 'type': 'console', 'cart_item_id': item.id, 'qty': item.qty, 'total': tot})
        elif item.itype == 'game': 
            ditem = get_object_or_404(game, id = item.itid)
            tot = ditem.price * item.qty
            s += tot
            print("price for item {} is {}".format(ditem.id, tot))
            fcrt.append({'item': ditem, 'type' : 'game', 'cart_item_id': item.id, 'qty': item.qty, 'total': tot})
    # print('fcart items: ', fcrt)
    request.session['s_val'] = s
    print("Cart Total: ",s)
    tx = s * 0.02
    gt = s + tx

    context = {}
    context['data'] = fcrt
    context['total'] = s
    context['tax'] = tx
    context['grndtot'] = gt
    return render(request, 'cart.html', context)

def updateqty(request, qv, cid):
    cart_item = Cart.objects.filter(id = cid).first()
    if cart_item:
        if qv == '1':
            if cart_item.qty < 5:
                cart_item.qty += 1      #increase the qunatity
            else:
                messages.warning(request, 'Maximum Limit reached!!')
        elif qv == '0':
            if cart_item.qty > 1:     #ensures the quantity do not go below 1
                cart_item.qty -= 1  #Decrease the qunatity
        cart_item.save()
    return redirect('/cart')

def remove(request, uid):
    cart_item = Cart.objects.filter(id = uid).first()
    # print('Cart items', c)
    if cart_item:
        cart_item.delete()
    return redirect('/cart')

# Order Conformation Page
def ordrconfo(request):
    userid = request.user.id
    citems = Cart.objects.filter(uid = request.user)
    oid = uuid.uuid4()      # Using UUID for a guaranteed unique order_id
    order_items = []

    
    for item in citems:
        product = None
        if item.itype == 'console':
            product = get_object_or_404(console, id=item.itid)
        elif item.itype == 'game':
            product = get_object_or_404(game, id=item.itid)  

        if product:
            Order.objects.create(order_id=oid, uid=request.user, itid=item.itid, itype= item.itype, qty= item.qty)
            item.delete()      #delete after placing order
            order_items.append({'product': product, 'type': item.itype, 'qty': item.qty})
    
    print(order_items)
    orders = Order.objects.filter(order_id= oid)
    s = sum(item['product'].price * item['qty'] for item in order_items)
    tx = s * 0.02
    gt = s + tx
    
    context = {}
    context['data'] = order_items
    context['total'] = s
    context['tax'] = tx 
    context['grndtot'] = gt 

    return render(request, 'orderconfo.html', context)

# Filter - price function
def range(request):
    context = {}
    context['show_reset_button'] = False
    min_val = request.GET['min']
    max_val = request.GET['max']
    # print('min', min_val)
    # print('max', max_val)
    allowed_templates = ['pcgames.html', 'psgames.html', 'nsgames.html', 'xbxgames.html', 'home.html', 'psconsole.html', 'xbxconsole.html', 'swchconsole.html']  #Ensures only the admin specified templates are passed for security
    template = request.GET.get('template', 'home.html')     #default to homepage if no template specified
    
    if template not in allowed_templates:
        template = 'home.html'  # Default to home if an invalid template is specified

    if not(min_val and max_val):
        return HttpResponseBadRequest("Both minimum and maximum values are required.")

    if 'min' in request.GET and 'max' in request.GET:
        min_val = request.GET['min']
        max_val = request.GET['max']
        context['show_reset_button'] = True
    
    q1 = Q(price__gte = min_val)
    q2 = Q(price__lte = max_val)
    q3 = Q(is_active=True)
    g = game.objects.filter(q1 & q2 & q3)
    c = console.objects.filter(q1 & q2 & q3)
    
    glist = list(g)
    tg = random.sample(glist, min(len(glist), 6))

    context['consoles'] = c
    context['games'] = g
    context['trgames'] = tg
    return render(request, template, context)

# Search Logic
def search(request):
    query = request.GET['query']
    if len(query) > 100:
        allconsole = console.objects.none()         #if search query is too big , don't search , to protect the algorithm        
        allgames = game.objects.none()              #if search query is too big , don't search, to protect the algorithm
    else:
        allconsole = console.objects.filter(name__icontains=query)
        allgames = game.objects.filter(title__icontains=query)
    prods = {}
    prods['allgames'] = allgames
    prods['allconsole'] = allconsole
    prods['query'] = query
    return render(request, 'search.html', prods)

# Payment Page
def makepayment(request):
    orders = Order.objects.filter(uid = request.user)
    s = 0
    order_ids = []

    for x in orders:
        if x.itype == 'console':
            item = get_object_or_404(console, id=x.itid)
        elif x.itype == 'game':
            item = get_object_or_404(game, id=x.itid)  
        
        s += item.price * x.qty
        order_ids.append(x.id)
    
    print('Total Amount: ',s)
 
    client = razorpay.Client(auth=("user", "key"))

    # Create payment order
    data = { "amount": s*100, "currency": "INR", "receipt": ','.join(map(str, order_ids)) }       #s*100 because s in rupees and api requires paise.
    payment = client.order.create(data = data)
    print("Total Payment: ", payment)

    # Delete orders after payment
    for order_id in order_ids:
        Order.objects.filter(id=order_id).delete()

    context = {}
    context['data'] = payment
    uemail = request.user.username
    context['uemail'] = uemail
    return render(request, 'pay.html', context)

# Thank You Page
def sendusermail(request):
    uemail = request.user.username
    send_mail(
    "Gamer's Hub - Order Placed Successfully!",
    "Your Order From Gamer's Hub Has Been Placed Successfully!!.",
    "sameermaitre07@gmail.com",
    [uemail],
    fail_silently=False,
    )
    return render(request, 'thanks.html')

# About Page
def about(request):
    return render(request,'about.html')