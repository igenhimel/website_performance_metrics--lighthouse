from django.shortcuts import render
from .models import PageScore
import requests
from django.template import RequestContext

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
        performance_score = None
        seo_score = None
        best_practice_score = None
        accessibility_score = None

    return {
        'performance_score': performance_score,
        "seo_score": seo_score,
        'best_practice_score': best_practice_score,
        'accessibility_score': accessibility_score,
    }

def cronjob():
       
        # You can retrieve the list of URLs from a JSON file
        # For simplicity, I'll create a list of URLs here
        url_list = [
            "https://www.rentbyowner.com/property/romantic-apartment-villa-in-dinajpur/HA-3212783349",
            "https://www.rentbyowner.com/property/it-s-a-mud-made-luxury-chalet-one-only-village-homestay-in-bangladesh-in-green-clam-environment/HA-3211835112",
            "https://www.rentbyowner.com/property/eque-heritage-hotel-resort/BC-7966645",
            "https://www.rentbyowner.com/property/what-a-beautiful-apartment-with-nice-view/HA-1219476212",
            "https://www.rentbyowner.com/property/81-m2-apartment-2-bedrooms-6-guests/HG-72897672678069",
        ]

        results = []

        # Fetch previous database results
        previous_results = list(PageScore.objects.all())

        # Iterate through the list of URLs and fetch scores and metrics
        for url in url_list:
            scores = get_scores_and_metrics(url)
            
            # Create a dictionary containing URL and scores
            result = {
                'performance_score': scores['performance_score'],
                'seo_score': scores['seo_score'],
                'best_practice_score': scores['best_practice_score'],
                'accessibility_score': scores['accessibility_score'],
            }

            results.append(result)

            # Check if we already have scores and metrics for this URL in the database
            # If you want to store this data in the database, you can do so here
            # For demonstration, I'm saving it in the PageScore model
            page_score = PageScore(
            performance_score = result['performance_score'],
            seo_score = result['seo_score'],
            best_practice_score = result['best_practice_score'],
            accessibility_score = result['accessibility_score'],
            )
            page_score.save()


def sum():
     a = 5
     b = 5

     result = a+b
     print(a+b)


