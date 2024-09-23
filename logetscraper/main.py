import logging as log
from datetime import datetime
from urllib.parse import urlparse

import psycopg2
import requests as r
from bs4 import BeautifulSoup

CARDLISTURL = "https://loget-card.jp/list_card.aspx"
DBSERVICE = "logetcardtrackerdb_service"


def findCards(soup):
    """Given a bs4 soup object, return a list of card Ids and their image. This is based on
    the structure of the HTML of the LoGet card list page.

    :param soup: A bs4 soup object of the LoGet card list page, parsed by html
    :type soup: b4s.soup
    :returns: A tuple of lists containing (cardIds, cardImg)
    :rtype: typle

    """

    cardIds = []
    cardImg = []

    for article in soup.find_all("article"):
        for a in article.find_all("a"):
            assert a["href"].startswith(
                "list.aspx?card="
            ), f"Unexpected URL format in finding card Ids: {a['href']}"
            u = urlparse(a["href"])[4].split("=")
            cardIds.append(u[1])

        for img in article.find_all("img"):
            assert img["src"].startswith(
                "./img/cards/"
            ), f"Unexpected URL format in finding card Ids: {img['src']}"
            v = img["src"].split("/")
            cardImg.append(v[-1])

    return (cardIds, cardImg)


def logetURLReconstructor(inputPart, typ):
    """Given a part of a LoGet URL, reconstruct the full URL based on the type of URL.

    :param inputPart: A part of a LoGet URL
    :type inputPart: str
    :param type: The type of URL to reconstruct. Options are 'card', 'map', img
    :type type: str
    :param typ: 
    :returns: A full URL based on the input part and type.
    :rtype: str

    """

    if typ == "card":
        return f"https://loget-card.jp/list.aspx?card={inputPart}"
    elif typ == "map":
        return f"https://loget-card.jp/list_map.aspx?card={inputPart}"
    elif typ == "img":
        return f"https://loget-card.jp/img/cards/{inputPart}"
    else:
        raise ValueError(f"Unexpected type of URL to reconstruct: {typ}")


def findCardName(cardURL):
    """Given a card URL, return the name of the card.

    :param cardURL: str
    :returns: str: The name of the card

    """

    response = r.get(cardURL)
    soup = BeautifulSoup(response.content, "html.parser")
    s = soup.find_all("section", class_="listA")

    assert len(s) == 1, f"Unexpected number of sections in finding card name: {len(s)}"

    head = s[0].find_all("h1")

    assert (
        len(head) == 1
    ), f"Unexpected number of h1 tags in finding card name: {len(head)}"

    return head[0].text


def findCardSpotLink(cardURL):
    """Given a card URL, return the spot map link of the card.

    :param cardURL: str
    :returns: str: The spot map link of the card

    """

    response = r.get(cardURL)
    soup = BeautifulSoup(response.content, "html.parser")
    s = soup.find_all("section", class_="listA")

    assert len(s) == 1, f"Unexpected number of sections in finding card name: {len(s)}"

    spot = s[0].find_all("div", class_="text_footer")

    assert (
        len(spot) == 1
    ), f"Unexpected number of a tags in finding card name: {len(spot)}"

    link = spot[0].find_all("a", target="_blank")

    assert (
        len(link) == 1
    ), f"Unexpected number of a links in finding card name: {len(link)}"

    return link[0]["href"]


def main():
    """ """
    log.basicConfig(
        level=log.INFO,
        filename=f"scrapper_{datetime.now()}.log",
        encoding="utf-8",
        format="%(asctime)s-%(levelname)s:%(message)s",
    )
    logger = log.getLogger(__name__)

    consoleHandler = log.StreamHandler()
    logger.addHandler(consoleHandler)

    logger.info(
        f"*****Starting to scrape LoGet card at {datetime.now()}, URL: {CARDLISTURL}*****"
    )

    logger.info(f"Connecting to database using service: {DBSERVICE}")
    conn = psycopg2.connect(service=DBSERVICE)
    cur = conn.cursor()
    cur.execute('SELECT "Id" FROM tracker_logetcards;')
    existingCardIds = [str(x[0]) for x in cur.fetchall()]
    logger.info(
        f"There are a total of {len(existingCardIds)} cards in the database already."
    )

    response = r.get(CARDLISTURL)
    logger.info(
        f"Response status code of the card list URL page: {response.status_code}"
    )
    soup = BeautifulSoup(response.content, "html.parser")

    cardIds, cardImgs = findCards(soup)
    assert len(cardIds) == len(
        cardImgs
    ), f"Number of card Ids and card images do not match: {len(cardIds)} vs {len(cardImgs)}"
    logger.info(f"Found a total of {len(cardIds)} cards in the card list page.")

    for cardId, cardImg in zip(cardIds, cardImgs):
        if cardId in existingCardIds:
            logger.info(f"Card {cardId} already exists in the database. Skipping.")
            continue

        cardURL = logetURLReconstructor(cardId, "card")
        mapURL = logetURLReconstructor(cardId, "map")
        imgURL = logetURLReconstructor(cardImg, "img")

        name = findCardName(cardURL)
        spotLink = findCardSpotLink(cardURL)

        logger.warning(f"Adding card {cardId} to the database.")
        cur.execute(
            'INSERT INTO tracker_logetcards ("Id", "Name", "Img", "SpotmapLink", "LoGetURL", "SpotWebsiteLink") VALUES (%s, %s, %s, %s, %s, %s);',
            (cardId, name, imgURL, mapURL, cardURL, spotLink),
        )
        conn.commit()

    logger.warning(f"Closing database connection.")
    cur.close()
    conn.close()
    logger.info(f"*****Finished scraping LoGet card at {datetime.now()}*****")


if __name__ == "__main__":
    main()
