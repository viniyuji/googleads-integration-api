from django.shortcuts import render
from google.ads.googleads.client import GoogleAdsClient
import datetime
from ControladoraGoogleAds.models import MktGoogleAds
from urllib.parse import urlparse
from urllib.parse import parse_qs
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def ControladoraGoogleAds(request):
    if (request.method == "GET"):
        ga_client = GoogleAdsClient.load_from_storage("./ControladoraGoogleAds/google-ads.yaml", version="v11")
        ga_service = ga_client.get_service("GoogleAdsService")

        customer_ids = []
        yesterday = datetime.date.today() - datetime.timedelta(days=1)

        query_2022_data = """
            SELECT
                campaign.id, campaign.name, campaign.status, campaign.start_date, campaign.end_date,
                ad_group.id, ad_group.name, ad_group.status,
                ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls,
                metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions,
                customer.descriptive_name, customer.id,
                segments.date
            FROM ad_group_ad
            WHERE segments.date BETWEEN '2022-01-01' AND '2022-09-07'
            ORDER BY campaign.id
        """

        query_yesterday_data = """
            SELECT
                campaign.id, campaign.name, campaign.status, campaign.start_date, campaign.end_date,
                ad_group.id, ad_group.name, ad_group.status,
                ad_group_ad.ad.id, ad_group_ad.ad.name, ad_group_ad.ad.final_urls,
                metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions,
                customer.descriptive_name, customer.id,
                segments.date
            FROM ad_group_ad
            WHERE segments.date = '{}'
            ORDER BY campaign.id
        """.format(yesterday)

        for id in customer_ids:
            response = ga_service.search_stream(customer_id=id, query=query_yesterday_data)
            for batch in response:                      
                for row in batch.results:
                    #cada row ?? um objeto parecido com .json
                    final_url = str(row.ad_group_ad.ad.final_urls)
                    params = parse_qs(urlparse(final_url).query)

                    if ('utm_content' in params.keys()):
                        utm_content = params['utm_content'][0]
                    else: utm_content = None

                    if ('utm_source' in params.keys()):
                        utm_source = params['utm_source'][0]
                    else: utm_source = None

                    if ('utm_campaign' in params.keys()):
                        utm_campaign = params['utm_campaign'][0]
                    else: utm_campaign = None

                    if ('utm_medium' in params.keys()):
                        utm_medium = params['utm_medium'][0]
                    else: utm_medium = None
                    
                    del params, final_url

                    MktGoogleAds.objects.create(
                        campaign_id = row.campaign.id,
                        campaign_name = row.campaign.name,
                        campaign_status = row.campaign.status,
                        campaign_start_date = row.campaign.start_date,
                        campaign_end_date = row.campaign.end_date,
                        group_id = row.ad_group.id,
                        group_name = row.ad_group.name,
                        group_status = row.ad_group.status,
                        ad_id = row.ad_group_ad.ad.id,
                        ad_name = row.ad_group_ad.ad.name,
                        ad_utm_source = utm_source,
                        ad_utm_medium = utm_medium,
                        ad_utm_campaign = utm_campaign,
                        ad_utm_content = utm_content,
                        impressions = row.metrics.impressions,
                        clicks = row.metrics.clicks,
                        cost = round(row.metrics.cost_micros/1000000, 2),
                        conversions = row.metrics.all_conversions,
                        date = row.segments.date,
                        account_name = row.customer.descriptive_name,
                        account_id = row.customer.id
                    )
        return JsonResponse({"status":"Success"})