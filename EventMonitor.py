import bs4, requests, smtplib, os, time
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
    """
    :param page: full page text in string format
    :param tag: the 'class' parameter in an html tag, preceded by a dot. Example:
    In this html tag: <h1 id="MembersFavouriteCount" class="favCount">551</h1>
    the search term is ".favCount"
    """
    raw = bs4.BeautifulSoup(page, 'html.parser')
    ticket_subset = raw.select(tag)[0].decode_contents()  # [3413:]
    return ticket_subset


def count_attending(page: str) -> int:
    raw = bs4.BeautifulSoup(page, 'html.parser')
    num_attending = raw.select('.favCount')[0].decode_contents()[1:]
    return num_attending


def send_email(body):
    conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
    conn.ehlo()  # call this to start the connection
    conn.starttls()  # starts tls encryption. When we send our password it will be encrypted.
    conn.login(fromAddress, os.environ['appkey'])
    conn.sendmail(fromAddress, toAddress, f'Subject: Unter Alert at {datetime.now().strftime("%H:%M:%S")}!\n\n{body}')
    conn.quit()
    print(f'Sent notification e-mails for the following recipients: {toAddress}')


def parse_page(page):
    subset = split_by_tag(page, '.ticket-list-item')
    num_ticket_releases = subset.count('release')
    current_closed_releases = subset.count('closed')

    if current_closed_releases < num_ticket_releases:
        send_email(f'''Subject: Tickets available ({datetime.now().strftime("%I:%M:%S %p")})!\n\n
        Number available: {4 - current_closed_releases}\n\n
        Raw text: {subset.encode('utf-8')}''')
        print("Tickets available! Sent email")
    else:
        print("No available tickets, did not send email")


if __name__ == '__main__':
    starttime = time.time()
    delay = 30.0

    while True:
        try:
            page = get_page(os.environ['page_url']).text
            print(f"polling {datetime.now()}. Current number of members attending: {count_attending(page)}")
            parse_page(page)
            time.sleep(delay - ((time.time() - starttime) % delay))
        except Exception as e:
            print(f"Unexpected exception: {e}")