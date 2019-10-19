### RATicketNotifier
Web scraping application that sends me an email when sold out tickets become reavailable

# How it works
RA uses an html tag of "closed" to represent sold out tickets. Note, there are often multiple ticket releases on the same event. My app parses the page and extracts the number of "closed" strings in the raw html. If this number drops (ie., one of the ticket releases becomes available) then it sends an email to let you know. The page url and email settings are controlled through environment variables. Made this primarily for my own use.
