from django.shortcuts import render
from .forms import URLForm
from .models import PageScore
import requests

def get_scores_and_metrics(url):
    # Make an HTTP request to the Lighthouse API
    lighthouse_url = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&category=performance&category=seo&category=best-practices&category=accessibility'
    response = requests.get(lighthouse_url)
    data = response.json()

    # Initialize scores with default values (in case data extraction fails)
    performance_score = 0
    seo_score = 0
    best_practice_score = 0
    accessibility_score = 0

    try:
        # Extract performance metrics and scores
        performance_score = data['lighthouseResult']['categories']['performance']['score'] * 100
        seo_score = data['lighthouseResult']['categories']['seo']['score'] * 100
        best_practice_score = data['lighthouseResult']['categories']['best-practices']['score'] * 100
        accessibility_score = data['lighthouseResult']['categories']['accessibility']['score'] * 100

        print(performance_score)
    except KeyError:
        # Handle the case where the expected keys are not present in the response
        pass

    return (
        performance_score,
        seo_score,
        best_practice_score,
        accessibility_score,
    )

def seo_checker(request):
    performance_score = None
    seo_score = None
    best_practice_score = None
    accessibility_score = None

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']

            # Check if we already have scores and metrics for this URL in the database
            page_score, created = PageScore.objects.get_or_create(url=url)

            if created:
                # If the scores and metrics don't exist, fetch them using the Lighthouse API
                (
                    performance_score,
                    seo_score,
                    best_practice_score,
                    accessibility_score,
                ) = get_scores_and_metrics(url)

                # Save the scores and metrics to the database
                page_score.performance_score = performance_score
                page_score.seo_score = seo_score
                page_score.best_practice_score = best_practice_score
                page_score.accessibility_score = accessibility_score
                page_score.save()
            else:
                # If the scores and metrics already exist in the database, use them
                performance_score = page_score.performance_score
                seo_score = page_score.seo_score
                best_practice_score = page_score.best_practice_score
                accessibility_score = page_score.accessibility_score
    else:
        form = URLForm()

    return render(request, 'seo_checker/seo_checker.html', {
        'form': form,
        'performance_score': performance_score,
        'seo_score': seo_score,
        'best_practice_score': best_practice_score,
        'accessibility_score': accessibility_score,
    })
