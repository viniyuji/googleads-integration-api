# googleads-integration-api
An API to get ads data from Google Ads platform. It's supposed to be used with a cron, scheduled to access the endpoint every day.
In order to work, you have to:
- Put the .env file in ./configs to be able to connect to the database
- Fill google-ads.yaml with your google account data. In this case, it has to contain:
	- developer_token
	- client_id
	- client_secret
	- refresh_token
	- use_proto_plus (set it to True)
	- login_customer_id (customer_id of your admin account)
- Put all your customer_ids in the tuple located in ./apps/ControladoraGoogleAds/views/list_ads.py
