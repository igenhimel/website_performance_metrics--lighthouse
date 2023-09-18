from django.shortcuts import render, redirect
from .forms import URLForm
from .models import PageScore
import requests

def get_scores_and_metrics(url):
    # Make an HTTP request to the Lighthouse API
    lighthouse_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=performance&category=seo&category=best-practices&category=accessibility'
    response = requests.get(lighthouse_url)
    data = response.json()
    try:
     performance_score = data['lighthouseResult']['categories']['performance']['score'] * 100
     seo_score = data['lighthouseResult']['categories']['seo']['score'] * 100
     best_practice_score = data['lighthouseResult']['categories']['best-practices']['score'] * 100
     accessibility_score = data['lighthouseResult']['categories']['accessibility']['score'] * 100
    except KeyError:
     performance_score=None
     seo_score =None
     best_practice_score =None
     accessibility_score=None

    return {
        'performance_score':performance_score,
        "seo_score":seo_score,
        'best_practice_score':best_practice_score,
        'accessibility_score':accessibility_score,
    }

def seo_checker(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            
            scores = get_scores_and_metrics(url)

            # Check if we already have scores and metrics for this URL in the database
            page_score = PageScore(
                 # Save the scores and metrics to the database
             performance_score = scores['performance_score'],
             seo_score = scores['seo_score'],
             best_practice_score = scores['best_practice_score'] ,
             accessibility_score = scores['accessibility_score']
            )
            page_score.save()
                
            return render(request,'seo_checker/seo_checker.html',scores)
               
    else:
        form = URLForm()
                

    return render(request, 'seo_checker/seo_checker.html', {'form': form})
