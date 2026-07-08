#!/usr/bin/env python3
"""
Social media post validation script.

Checks character count against platform limits, hashtag count against best practice
ranges, and identifies URLs that count toward character limits.
"""

import re
import sys
from typing import Literal

Platform = Literal["twitter", "linkedin", "instagram"]


# Platform limits and hashtag best practices
PLATFORM_LIMITS = {
    "twitter": {"max_length": 280, "hashtag_range": (1, 2)},
    "linkedin": {"max_length": 3000, "hashtag_range": (3, 5)},
    "instagram": {"max_length": 2200, "hashtag_range": (5, 15)},
}


def count_urls(text: str) -> int:
    """Count URLs in the text using a regex pattern."""
    # Matches http://, https://, and t.co style URLs
    url_pattern = r"https?://[^\s]+"
    urls = re.findall(url_pattern, text)

    # Also match t.co shortened URLs without explicit protocol
    tco_pattern = r"\bt\.co\/[a-zA-Z0-9]+"
    tco_urls = re.findall(tco_pattern, text)

    return len(urls) + len(tco_urls)


def count_hashtags(text: str) -> int:
    """Count hashtags in the text."""
    hashtag_pattern = r"#\w+"
    return len(re.findall(hashtag_pattern, text))


def validate_post(text: str, platform: Platform) -> dict:
    """
    Validate a social media post against platform-specific rules.

    Returns a dict with validation results:
    - char_count: total character count
    - url_count: number of URLs found
    - hashtag_count: number of hashtags found
    - char_status: "ok" or "exceeded" with platform limit
    - hashtag_status: "ok" or "outside_range" with recommended range
    - urls_flagged: list of URLs found (for Twitter/X awareness)
    """
    config = PLATFORM_LIMITS[platform]
    char_count = len(text)
    url_count = count_urls(text)
    hashtag_count = count_hashtags(text)

    # Character count validation
    char_status = "ok" if char_count <= config["max_length"] else "exceeded"

    # Hashtag validation
    min_tags, max_tags = config["hashtag_range"]
    hashtag_status = (
        "ok"
        if min_tags <= hashtag_count <= max_tags
        else "outside_range"
    )

    # Extract URLs for flagging
    url_pattern = r"https?://[^\s]+"
    urls_flagged = re.findall(url_pattern, text)

    tco_pattern = r"\bt\.co\/[a-zA-Z0-9]+"
    urls_flagged.extend(re.findall(tco_pattern, text))

    return {
        "platform": platform,
        "char_count": char_count,
        "char_limit": config["max_length"],
        "url_count": url_count,
        "hashtag_count": hashtag_count,
        "hashtag_range": config["hashtag_range"],
        "char_status": char_status,
        "hashtag_status": hashtag_status,
        "urls_flagged": urls_flagged,
    }


def format_report(result: dict) -> str:
    """Format validation results as a human-readable report."""
    lines = [
        f"Platform: {result['platform'].title()}",
        f"Character count: {result['char_count']}/{result['char_limit']}",
        f"URL count: {result['url_count']}",
        f"Hashtag count: {result['hashtag_count']} (recommended: {result['hashtag_range'][0]}-{result['hashtag_range'][1]})",
        "",
    ]

    if result["char_status"] == "exceeded":
        lines.append(
            f"[WARNING] Character limit exceeded by {result['char_count'] - result['char_limit']} characters"
        )
    else:
        lines.append("[OK] Character count within limit")

    if result["hashtag_status"] == "outside_range":
        lines.append("[WARNING] Hashtag count outside recommended range")
    else:
        lines.append("[OK] Hashtag count within recommended range")

    if result["urls_flagged"]:
        lines.append("")
        lines.append(f"[INFO] URLs detected ({len(result['urls_flagged'])}):")
        for url in result["urls_flagged"]:
            lines.append(f"  - {url}")
        if result["platform"] == "twitter":
            lines.append("  Note: URLs count as 23 characters each on Twitter/X")

    return "\n".join(lines)


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 3:
        print("Usage: python validate_post.py <platform> <text>")
        print("Platforms: twitter, linkedin, instagram")
        sys.exit(1)

    platform_arg = sys.argv[1].lower()
    text = " ".join(sys.argv[2:])

    if platform_arg not in PLATFORM_LIMITS:
        print(f"Unknown platform: {platform_arg}")
        print(f"Available: {', '.join(PLATFORM_LIMITS.keys())}")
        sys.exit(1)

    result = validate_post(text, platform_arg)  # type: ignore
    print(format_report(result))

    # Exit with error code if validations failed
    if result["char_status"] == "exceeded" or result["hashtag_status"] == "outside_range":
        sys.exit(1)


if __name__ == "__main__":
    main()