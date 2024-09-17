from django.contrib import admin
from .models import Bid,Comment,Watchlist,Listing,Category,User

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',) 

   
    ordering = ('name',)  
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'starting_bid', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'category')
    
class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'bidder', 'amount', 'bid_time')
    search_fields = ('listing__title', 'bidder__username', 'amount')
    list_filter = ('listing', 'bidder', 'bid_time')


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
   

class UsersAdmin(admin.ModelAdmin):
    list_display= ('username','first_name','last_name')
# Register your models here.
admin.site.register(User,UsersAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist,WatchlistAdmin)
admin.site.register(Listing,ListingAdmin)
