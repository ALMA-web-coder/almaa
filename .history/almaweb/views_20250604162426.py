from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Article 
from .models import News , Acca

def acca(request):
    fundamental_programs = Acca.objects.filter(level='FUNDAMENTAL')
    applied_skills_programs = Acca.objects.filter(level='APPLIED_SKILLS')
    strategic_programs = Acca.objects.filter(level='STRATEGIC_PROFESSIONAL')

    context = {
        'fundamental_programs': fundamental_programs,
        'applied_skills_programs': applied_skills_programs,
        'strategic_programs': strategic_programs,
    }
    return render(request, 'application/acca.html', context)

def home(request):
    # Fetch all news items, ordered by date_posted (latest first)
    latest_news = News.objects.all().order_by('-date_posted')
    #Fetch all Acca programs, ordered by level
    
    # Render the home page with the latest news context
    return render(request, 'information/home.html', {'latest_news': latest_news})

def news_list(request): 
    news_items = News.objects.all().order_by('-date_posted') 
    return render(request, 'information/news_list.html', {'news_items': news_items})  
def news_detail(request, news_id):
    news_item = News.objects.get(id=news_id)    
    return render(request, 'information/news_detail.html', {'news_item': news_item})  




def Journal(request):
    articles = Article.objects.all()  # Fetching all articles from the database
    return render(request, 'information/journals.html', {'articles': articles})  # Passing the articles to the template
  
def download_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    response = HttpResponse(article.document, content_type='application/pdf')  # Change content_type if necessary
    response['Content-Disposition'] = f'attachment; filename="{article.document.name}"'
    return response

def Consultancy(request):
  return render(request, 'information/consultancy_unit.html')


def Payment(request):
  return render(request, 'information/home.html')


def About(request):
  return render(request, 'information/about_us.html')


def Agribusiness(request):
  return render(request, 'programs/agri_business.html')



def MBA(request):
  return render(request, 'programs/mba.html')


def CLM(request):
  return render(request, 'programs/clm.html')

def MGov(request):
  return render(request, 'programs/mgov.html')

def BTLGS(request):
  return render(request, 'programs/btlgs.html')


def ILF(request):
  return render(request, 'programs/ilf.html')




