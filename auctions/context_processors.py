# auctions/context_processors.py
from .models import Category,Watchlist

def categories_processor(request):
    categories = Category.objects.all()
    print(categories)
    return {'categories': categories}


def watchlist_count(request):
    if request.user.is_authenticated:
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
    else:
        watchlist_count = 0
    
    return {
        'watchlist_count': watchlist_count  
    }
