import bs4, requests, smtplib, os
from datetime import datetime

# ------------------- E-mail list ------------------------
fromAddress = os.environ['email_address']
toAddress = os.environ['email_address']
# --------------------------------------------------------


"""
Scrapes page and splits html response
Counts the number of "closed" instances on the page
If the number of closed instances decreases (ie a ticket
becomes available), send an email.
"""


def get_page(url: str):
    page = requests.get(url)
    page.raise_for_status()
    return page


def split_by_tag(page: str, tag: str) -> str:
    raw = bs4.BeautifulSoup(page, 'html.parser')
    ticket_subset = raw.select(tag)[0].decode_contents()  # [3413:]
    return ticket_subset


def send_email(body):
    conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
    conn.ehlo()  # call this to start the connection
    conn.starttls()  # starts tls encryption. When we send our password it will be encrypted.
    conn.login(fromAddress, os.environ['appkey'])
    conn.sendmail(fromAddress, toAddress, f'Subject: Unter Alert at {datetime.now().strftime("%H:%M:%S")}!\n\n{body}')
    conn.quit()
    print(f'Sent notification e-mails for the following recipients: {toAddress}')


if __name__ == '__main__':
    page = get_page(os.environ['page'])
    subset = split_by_tag(page.text, ".ticket-list-item")
    freq = subset.count("closed")

    if freq == 4:
        send_email(f'''Subject: Tickets available ({datetime.now().strftime("%H:%M:%S")})!\n\n
        Number available: {4 - freq}''')
