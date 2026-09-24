from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url: str) -> str:
    parsed_url = urlsplit(url)
    full_path  = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()


def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1_tag = soup.find("h1")
    h2_tag = soup.find("h2")

    if h1_tag:
        return h1_tag.get_text(strip=True)
    elif h2_tag:
        return h2_tag.get_text(strip=True)
    return ""

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main_tag = soup.find("main")

    if isinstance(main_tag, Tag):
        p_tag = main_tag.find("p")
    else:
        p_tag = soup.find("p")

    return p_tag.get_text(strip=True) if isinstance(p_tag, Tag) else ""

def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []

    for anchor in soup.find_all("a"):
        if not isinstance(anchor, Tag):
            continue

        href = anchor.get("href")
        if isinstance(href, str) and href:
            try:
                absolute = urljoin(base_url, href)
                urls.append(absolute)
            except Exception as e:
                print(f"{str(e)}: {e}")

    return urls

def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    images = []

    for img in soup.find_all("img"):
        if not isinstance(img, Tag):
            continue

        src = img.get("src")
        if isinstance(src, str) and src:
            try:
                absolute = urljoin(base_url, src)
                images.append(absolute)
            except Exception as e:
                print(f"{str(e)}: {e}")
            
    return images

def extract_page_data(html: str, page_url: str) -> PageData:
    return PageData(
        url=page_url,
        heading=get_heading_from_html(html),
        first_paragraph=get_first_paragraph_from_html(html),
        outgoing_links=get_urls_from_html(html, page_url),
        image_urls=get_images_from_html(html, page_url)
    )
