from django.db import models

class MktGoogleAds(models.Model):
    mkt_google_ads_id = models.AutoField(primary_key=True)
    campaign_id = models.IntegerField(blank=True, null=True)
    campaign_name = models.CharField(max_length=200, blank=True, null=True)
    campaign_status = models.IntegerField(blank=True, null=True)
    campaign_start_date = models.DateField(blank=True, null=True)
    campaign_end_date = models.DateField(blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)
    group_name = models.CharField(max_length=200, blank=True, null=True)
    group_status = models.IntegerField(blank=True, null=True)
    ad_id = models.IntegerField(blank=True, null=True)
    ad_name = models.CharField(max_length=200, blank=True, null=True)
    ad_utm_source = models.CharField(max_length=200, blank=True, null=True)
    ad_utm_medium = models.CharField(max_length=200, blank=True, null=True)
    ad_utm_campaign = models.CharField(max_length=200, blank=True, null=True)
    ad_utm_content = models.CharField(max_length=200, blank=True, null=True)
    impressions = models.IntegerField(blank=True, null=True)
    clicks = models.IntegerField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    conversions = models.FloatField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    account_name = models.CharField(max_length=200, blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mkt_google_ads'
