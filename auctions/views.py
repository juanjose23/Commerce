from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Listing, Bid, Watchlist, Comment,Category


def index(request):
    
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    active_listings = Listing.objects.filter(status=1)
    listcategories = Category.objects.filter(listings__in=active_listings).distinct()
    listings = active_listings
    
    if category_id:
        listings = listings.filter(category_id=category_id)
    
    if min_price:
        listings = listings.filter(starting_bid__gte=min_price)
    
    if max_price:
        listings = listings.filter(starting_bid__lte=max_price)
    watchlist = []  # Inicializa como lista vacía
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).values_list('listing', flat=True)
    context = {
        'listings': listings,
        'listcategories': listcategories,
        'watchlist': watchlist,
    }
    
    return render(request, 'auctions/index.html', context)

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    listings = Listing.objects.filter(category=category)
    return render(request, 'auctions/category_list.html', {'category': category, 'listings': listings})
 
def prueba(request):
    
    return render(request, "prueba.html")
@login_required
def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        starting_bid = request.POST.get('starting_bid')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

       
        if not title or not description or not starting_bid:
            return render(request, 'auctions/create_listing.html', {
                'error': 'Title, description, and starting bid are required.',
                'categories': Category.objects.all()
            })
        
        try:
            starting_bid = float(starting_bid)
        except ValueError:
            return render(request, 'auctions/create_listing.html', {
                'error': 'Starting bid must be a valid number.',
                'categories': Category.objects.all()
            })

        category = Category.objects.filter(id=category_id).first()
        if category_id and not category:
            return render(request, 'auctions/create_listing.html', {
                'error': 'Invalid category selected.',
                'categories': Category.objects.all()
            })

       
        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image=image,
            category=category,
            created_by=request.user
        )
        listing.save()
        return redirect('index')

    else:
        
        return render(request, 'auctions/create_listing.html', {
            'categories': Category.objects.all()
        })

@login_required
def listing_detail(request, slug):
   
    listing = get_object_or_404(Listing, slug=slug)
    
   
    bids = listing.bids.all().order_by('-bid_time')
    comments=listing.comments.all().order_by('-created_at')
    is_in_watchlist = False
    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
     # Mensaje de ganador
    winner_message = None
    if listing.status == 2:  # Suponiendo que 2 significa que la subasta está cerrada
        highest_bid = bids.first()  # La oferta más alta es la primera en la lista ordenada
        if highest_bid:
            winner_message = f"The auction is closed. The winner is {highest_bid.bidder.username} with a bid of ${highest_bid.amount}."
        else:
            winner_message = "The auction is closed, but no bids were placed."
    
    context = {
        'listing': listing,
        'bids': bids,
        'comments':comments,
        'is_in_watchlist': is_in_watchlist,
        'winner_message':winner_message,
    }
    return render(request, 'auctions/listing_detail.html', context)


@login_required
def create_bid(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            try:
                amount = float(amount)
                if amount <= 0:
                  
                    messages.error(request, "Bid amount must be greater than zero.")
                    return redirect('listing_detail', slug=listing.slug)
                if amount < listing.current_price():
                    messages.error(request, f"Bid amount must be greater than the current price of {listing.current_price()}.")
                    return redirect('listing_detail', slug=listing.slug)  
                bid = Bid(listing=listing, bidder=request.user, amount=amount)
                bid.save()
                messages.success(request, "Your bid has been placed successfully.")
                return redirect('listing_detail', slug=listing.slug)  # Redirige a la página de detalles del listado
            except ValueError as e:
                # Maneja errores, como cantidades inválidas
                return  redirect('listing_detail', slug=listing.slug)
               

    return  redirect('listing_detail', slug=listing.slug)

@login_required
def finish_auction(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.user == listing.created_by:
        listing.status = 2
        listing.save()
        return redirect('listing_detail', slug=listing.slug)
    else:
        return redirect('listing_detail', slug=listing.slug)
    
@login_required
def create_comment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment(listing=listing, user=request.user, content=content)
            comment.save()
            messages.success(request, "Your comment successfully.")
            return redirect('listing_detail', slug=listing.slug)  
    return redirect('listing_detail', slug=listing.slug)  

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, listing=listing)

    if not created:
        watchlist_item.delete()
        message = "Removed from Watchlist"
    else:

        message = "Added to Watchlist"
    messages.success(request, message)
    referer_url = request.META.get('HTTP_REFERER', '/')
    return redirect(referer_url)

@login_required
def wathclist(request):
    wathclist = Watchlist.objects.filter(user=request.user).select_related('listing').all()
    watchlist_ids = Watchlist.objects.filter(user=request.user).values_list('listing__id', flat=True)
    
    context = {
        'wathclist': wathclist,
        'watchlist': watchlist_ids, 
    }
    return render(request, 'auctions/watchlist.html', context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    


