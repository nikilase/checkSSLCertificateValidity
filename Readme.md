# SSL Certificate Expiry Checker and Email Alert
Tool to check if an SSL Certificate is near expiry and send an email alert if it is.
This acts as a quick and dirty way of replacing the email service from Letsencrypt which is about to be deprecated.

You need to create and configure `config/config.toml`from the template file. 

It is advised to run this in a venv (virtual environment) using python 3.12 and the requirements specified in 
the `requirements.txt` file.

This tool is intended to be run once a day using cron (or other alternatives such as a timed linux service or the 
windows task scheduler).

## What does this do
Preconfigured this tool sends an email alert 4, 3, 2, and 1 week before the expiry of an SSL Cert.
It also then proceeds to send an email with the high priority flag set each day when the expiry is in less than a week.

This tool can use two underlying strategies to ascertain how long a certificate is valid.
Both methods can be used at the same time, though you might get duplicate mails.

### crt.sh based
It can use the crt.sh website which in turn uses the Certificate Transparency (CT) Logs to get all non expired certificates 
of the requested certificate name. There we can get the most current certificate and check for the expiry date.
If none are returned we know the certificate name is either invalid or there is no non expired certificate.
Keep in mind the CT Logs are not real time and might have a delay of a couple of minutes.

### website based
This only works if you have access to a website running the SSL Certificate in question. 
It works by requesting the website and hence the Certificate of the website. There we can calculate for how long the 
certificate will stay valid.