# RATicketNotifier
Web scraping application that sends an email when sold out tickets become reavailable

###Motivation
When an event on Resident Advisor sells out, they offer an official resale channel through their website. When someone gives up their ticket, the button on their site switches from sold out to available, but there's otherwise no notification that more tickets have become available. Often many hours or days go by between ticket resales. To avoid refreshing the page regularly and hoping to get lucky, I opted to write this script to scrape the page every minute and email me if a ticket becomes available.

Their website offers another useful feature that lists the number of members attending a given event. I noticed that when tickets are resold, the member count doesn't go down - so this can be used as a soft check on whether this application is working properly. So if the number of members attending increases, you know that someone sold a ticket. Though, if someone who already has a ticket buys another, the member count does not increase. 

### How it works
RA uses an html tag of "closed" to represent sold out tickets. Note, there are often multiple ticket releases on the same event. My app parses the page and extracts the number of "closed" strings in the raw html. If this number drops (ie., one of the ticket releases becomes available) then it sends an email to let you know. The page url and email settings are controlled through environment variables. Made this primarily for my own use.

### How to use
Add your email_address, password (recommended to use appkey instead) and the url of the event to your env variables. Then run scraper.py. Feel free to customize the email you send to yourself.