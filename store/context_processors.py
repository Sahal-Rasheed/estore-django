from .models import Category

def nav_category(request):
    nav_categ = Category.objects.all()
    return dict(nav_categ=nav_categ)