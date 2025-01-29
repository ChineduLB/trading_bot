
class CoinbaseApiSecret(object):
    CoinbaseApiKey = ""
    CoinbasePassphrase = ""
    CoinbaseSecret = ""
    TradingViewAlertSecret = ""
    AlertsDatabase = ""
    AlertsDBPassword = ""
    AlertsDBUser = ""
    DBInstanceConnName = ""
    KuCoinApiKey = ""
    KuCoinPassphrase = ""
    KuCoinSecret = ""
    KuCoinSubAcctsPwd = ""
    KuCoinLbCrypto2000ApiSecret = ""
    KuCoinLbCrypto2000ApiKey = ""
    KuCoinLbCrypto3000ApiSecret = ""
    KuCoinLbCrypto3000ApiKey = ""
    KuCoinLbCrypto4000ApiSecret = ""
    KuCoinLbCrypto4000ApiKey = ""
    EMAIL_API_KEY = ""
    CoinbaseLbCrypto2000ApiKey = ""
    CoinbaseLbCrypto2000ApiSecret = ""
    CoinbaseLbCrypto1000ApiKey = ""
    CoinbaseLbCrypto1000ApiSecret = ""
    CoinbaseLbCrypto4000ApiKey = ""
    CoinbaseLbCrypto4000ApiSecret = ""
    CoinbasePortfolioPassPhrase = ""
    LbCrypto5000CbApiKey = ""
    LbCrypto5000CbApiSecret = ""
    LbCrypto7000CbApiKey = ""
    LbCrypto7000CbApiSecret = ""
    LbCrypto8000CbApiKey = ""
    LbCrypto8000CbApiSecret = ""
    LbCrypto9000CbApiKey = ""
    LbCrypto9000CbApiSecret = ""
    LbCrypto1100CbApiKey = ""
    LbCrypto1100CbApiSecret = ""
    LbCrypto1200CbApiKey = ""
    LbCrypto1200CbApiSecret = ""
    KuCoinLbCrypto5000ApiKey = ""
    KuCoinLbCrypto5000ApiSecret = ""
    KuCoinLbCrypto7000ApiKey = ""
    KuCoinLbCrypto7000ApiSecret = ""
    KuCoinLbCrypto8000ApiKey = ""
    KuCoinLbCrypto8000ApiSecret = ""
    KuCoinLbCrypto1000ApiKey = ""
    KuCoinLbCrypto1000ApiSecret = ""
    LbCrypto9000KCApiKey = ""
    LbCrypto9000KCApiSecret = ""

    SecretNames = ["CoinbaseApiKey", "CoinbasePassphrase", "CoinbaseSecret",
                   "TradingViewAlertSecret", "AlertsDatabase", "AlertsDBPassword",
                   "AlertsDBUser", "DBInstanceConnName", "KuCoinApiKey",
                   "KuCoinPassphrase", "KuCoinSecret", "KuCoinSubAcctsPwd",
                   "KuCoinLbCrypto2000ApiSecret", "KuCoinLbCrypto2000ApiKey",
                   "KuCoinLbCrypto3000ApiSecret", "KuCoinLbCrypto3000ApiKey",
                   "KuCoinLbCrypto4000ApiSecret", "KuCoinLbCrypto4000ApiKey",
                   "EMAIL_API_KEY", "CoinbaseLbCrypto2000ApiKey",
                   "CoinbaseLbCrypto2000ApiSecret", "CoinbaseLbCrypto1000ApiKey",
                   "CoinbaseLbCrypto1000ApiSecret", "CoinbaseLbCrypto4000ApiKey",
                   "CoinbaseLbCrypto4000ApiSecret",  "CoinbasePortfolioPassPhrase",
                   "LbCrypto5000CbApiKey", "LbCrypto7000CbApiKey", "LbCrypto8000CbApiKey",
                   "LbCrypto5000CbApiSecret", "LbCrypto7000CbApiSecret", "LbCrypto8000CbApiSecret",
                   "LbCrypto9000CbApiKey", "LbCrypto9000CbApiSecret", "LbCrypto1100CbApiKey",
                   "LbCrypto1100CbApiSecret", "LbCrypto1200CbApiKey", "LbCrypto1200CbApiSecret",
                   "KuCoinLbCrypto5000ApiKey",    "KuCoinLbCrypto5000ApiSecret",
                   "KuCoinLbCrypto7000ApiKey",    "KuCoinLbCrypto7000ApiSecret",
                   "KuCoinLbCrypto8000ApiKey",    "KuCoinLbCrypto8000ApiSecret",
                   "KuCoinLbCrypto1000ApiKey",    "KuCoinLbCrypto1000ApiSecret",
                   "LbCrypto9000KCApiKey",  "LbCrypto9000KCApiSecret",
                   ]


secretCls = None

def get_coinbase_secrets():
    global secretCls
    if secretCls is None:
        from google.cloud import secretmanager

        # Data Class for transporting scret
        secretCls = CoinbaseApiSecret()

        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # for key in secrets_map.keys():
        for name in secretCls.SecretNames:
            # Build the resource name of the secret version.
            secretversion = "projects/tradingviewwebhooks-338018/secrets/{0}/versions/latest".format(name)
            response = client.access_secret_version(request={"name": secretversion})
            setattr(secretCls, name, response.payload.data.decode("UTF-8"))

    return secretCls


if __name__ == "__main__":
    scl = get_coinbase_secrets()
    print(scl)
