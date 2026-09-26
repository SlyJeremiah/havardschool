import re
from urllib.parse import quote

from django import template

register = template.Library()

YOUTUBE_RE = re.compile(r"(?:youtube\.com/(?:watch\?v=|shorts/|embed/)|youtu\.be/)([\w-]{11})")


@register.filter
def video_embed_url(url):
    """Turn a YouTube or Facebook video/reel URL into an iframe-embeddable URL."""
    if not url:
        return ""
    if m := YOUTUBE_RE.search(url):
        return f"https://www.youtube-nocookie.com/embed/{m.group(1)}"
    if "facebook.com" in url or "fb.watch" in url:
        return f"https://www.facebook.com/plugins/video.php?href={quote(url, safe='')}&show_text=false"
    return ""


@register.filter
def paragraphs(text):
    """Split text on blank lines."""
    return [p.strip() for p in re.split(r"\n\s*\n", text or "") if p.strip()]
