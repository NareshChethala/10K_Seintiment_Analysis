# clean_filing_html.py

from bs4 import BeautifulSoup

def clean_filing_html(filing_html):
    """
    Cleans the full HTML of a 10-K filing to extract readable plain text.
    Removes scripts, styles, and unnecessary whitespace.

    Args:
        filing_html (str): Raw HTML string of the filing document.

    Returns:
        str: Cleaned plain text extracted from the HTML.
    """
    try:
        soup = BeautifulSoup(filing_html, "html.parser")

        # Remove unwanted tags
        for tag in soup(["script", "style", "header", "footer", "nav", "noscript"]):
            tag.decompose()

        # Extract text from the body if present
        body = soup.find("body")
        raw_text = body.get_text(separator="\n") if body else soup.get_text(separator="\n")

        # Normalize whitespace
        lines = [line.strip() for line in raw_text.splitlines()]
        clean_text = "\n".join(line for line in lines if line)

        return clean_text

    except Exception as e:
        print(f"❌ Error cleaning HTML: {e}")
        return ""
