# webhook_interface
Simple example of facebook webhook interface using python and flask

## Save your page token as an environment variable
It is recommended that you keep sensitive information like your page access token secure by not hardcoding it into your webhook.

To do this, add the following to your environment variables, where <PAGE_ACCESS_TOKEN> is the access token you have just generated and <VERIFY_TOKEN> is a random string that you set to verify your webhook:

<!-- .env -->
```
PAGE_ACCESS_TOKEN="<PAGE_ACCESS_TOKEN>"
VERIFY_TOKEN="<VERIFY_TOKEN>"
```
Live edit in [Glitch.com](https://glitch.com/edit/#!/gleaming-broadleaf-trouble)