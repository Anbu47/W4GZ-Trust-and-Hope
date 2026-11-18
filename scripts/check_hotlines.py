"""Compare the game's hotline contacts with Find A Helpline after a main push."""
import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

DIRECTORY = "https://findahelpline.com/countries/vn"
STATUS_BRANCH = "hotline-checks"
PROFILES = {
    "mai": ("Ngày Mai", "ngay mai", "ngay-mai", "duongdaynongngaymai.vn"),
    "hope": ("HOPE", "hope suicide prevention hotline", "hope-suicide-prevention-hotline", "hyvongsong.com"),
    "child": ("Tổng đài Quốc gia Bảo vệ Trẻ em", "national child helpline", "t-ng-dai-di-n-tho-i-qu-c-gia-b-o-v-tr-em-national-child-helpline", "tongdai111.vn"),
    "csaga": ("CSAGA", "duong day nong ho tro nguoi bi bao luc gioi", "d-ng-day-nong-h-tr-ng-i-b-b-o-l-c-gi-i", "csaga.org.vn"),
    "peace": ("Ngôi nhà Bình yên", "ngoi nha binh yen", "ngoi-nha-binh-yen-peace-house-shelter-vietnam", "cwd.vn"),
}
# HOPE's opening hours are not published in its directory profile. Do not claim
# this check verifies them. The other four profiles do publish hours.
HOURS = {
    "mai": ([r"1:00\s*p\.?\s*m\.?", r"8:30\s*p\.?\s*m\.?", r"Wednesday\s+to\s+Sunday"], ["13:00", "20:30"]),
    "child": ([r"24\s*/\s*7"], ["24/7"]),
    "csaga": ([r"0?8:00\s*a\.?\s*m\.?", r"9:00\s*p\.?\s*m\.?"], ["08:00", "21:00"]),
    "peace": ([r"24\s*/\s*7"], ["24/7"]),
}


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.parts, self.links, self.skip = [], [], 0
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.skip += 1
        if not self.skip:
            self.parts.append(" ")
            if tag == "a" and attrs.get("href"):
                self.links.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1
        if not self.skip:
            self.parts.append(" ")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)

    @property
    def text(self):
        return re.sub(r"\s+", " ", "".join(self.parts)).strip()


class Cards(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.cards, self.current, self.bold = [], None, False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "p":
            self.current = {"title": "", "text": "", "phones": []}
        if self.current is not None:
            if tag == "b":
                self.bold = True
            if tag == "a" and attrs.get("href", "").startswith("tel:"):
                self.current["phones"].append(attrs["href"].split("?", 1)[0][4:])

    def handle_endtag(self, tag):
        if tag == "b":
            self.bold = False
        if tag == "p" and self.current is not None:
            if self.current["title"]:
                self.cards.append(self.current)
            self.current = None

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data + " "
            if self.bold:
                self.current["title"] += data


def normalized(value):
    value = unicodedata.normalize("NFKD", value.lower().replace("đ", "d"))
    return re.sub(r"[^a-z0-9]+", " ", "".join(c for c in value if not unicodedata.combining(c))).strip()


def contains_phone(text, number):
    digits = re.sub(r"\D", "", number)
    if digits.startswith("84") and len(digits) > 10:
        digits = digits[2:]
    if digits.startswith("0"):
        digits = digits[1:]
    for variant in (digits, "0" + digits, "84" + digits):
        pattern = r"(?<!\d)" + r"[\s().+\-]*".join(variant) + r"(?!\d)"
        if re.search(pattern, text):
            return True
    return False


def download(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "TrustAndHope-contact-check/1.0", "Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=25) as response:
                raw = response.read(3_000_001)
            if len(raw) > 3_000_000:
                raise ValueError("Source page exceeds size limit")
            return raw.decode("utf-8")
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def read_support(path):
    source = Path(path).read_text(encoding="utf-8")
    match = re.search(r"^const PART0_SUPPORT = (.*);$", source, re.M)
    if not match:
        raise ValueError("Cannot find the game's support information")
    support = json.loads(match[1])
    cards = Cards(support).cards
    return support, cards


def verify(index_path, loader=download):
    support, cards = read_support(index_path)
    country = Page(loader(DIRECTORY))
    country_text = normalized(country.text)
    positions = {}
    for ident, (_, alias, slug, _) in PROFILES.items():
        if not any("/organizations/" + slug in link for link in country.links):
            raise ValueError("Directory listing missing: " + ident)
        position = country_text.find(alias)
        if position < 0:
            raise ValueError("Directory name missing: " + ident)
        positions[ident] = position
    issues, checks = [], []
    for ident, (title, _, slug, host) in PROFILES.items():
        card = next((c for c in cards if c["title"].startswith(title)), None)
        if not card or not card["phones"]:
            issues.append("Game contact card missing: " + ident)
            continue
        # Keep telephone matching inside this provider's directory listing.
        start = positions[ident]
        end = min((pos for pos in positions.values() if pos > start), default=len(country_text))
        segment = country_text[start:end]
        bad_phones = [p for p in card["phones"] if not contains_phone(segment, p)]
        profile_url = "https://findahelpline.com/organizations/" + slug
        profile = Page(loader(profile_url))
        website_ok = any((urllib.parse.urlparse(link).hostname or "").removeprefix("www.") == host for link in profile.links)
        if bad_phones:
            issues.append("Phone number changed or missing: " + ident)
        if not website_ok:
            issues.append("Official website changed or missing: " + ident)
        hours_status = "not_published_in_profile"
        if ident in HOURS:
            patterns, labels = HOURS[ident]
            hours_ok = all(re.search(p, profile.text, re.I) for p in patterns) and all(label in card["text"] for label in labels)
            hours_status = "matched" if hours_ok else "needs_review"
            if not hours_ok:
                issues.append("Opening hours changed or cannot be confirmed: " + ident)
        checks.append({"id": ident, "name": title, "phones": card["phones"], "phone_match": not bad_phones, "website_match": website_ok, "hours": hours_status, "source": profile_url})
    return {"status": "passed" if not issues and len(checks) == 5 else "needs_review", "issues": issues, "checks": checks, "support_sha256": hashlib.sha256(support.encode("utf-8")).hexdigest()}


def github(method, endpoint, data=None):
    repo, token = os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_TOKEN"]
    request = urllib.request.Request("https://api.github.com/repos/" + repo + endpoint, method=method, data=json.dumps(data).encode() if data is not None else None, headers={"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json", "Content-Type": "application/json", "User-Agent": "TrustAndHope-contact-check"})
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)


def publish(report):
    try:
        github("GET", "/git/ref/heads/" + STATUS_BRANCH)
    except urllib.error.HTTPError as exc:
        if exc.code != 404:
            raise
        try:
            github("POST", "/git/refs", {"ref": "refs/heads/" + STATUS_BRANCH, "sha": os.environ["GITHUB_SHA"]})
        except urllib.error.HTTPError as conflict:
            if conflict.code != 422:
                raise
    for attempt in range(3):
        previous, sha = {}, None
        try:
            item = github("GET", "/contents/status.json?ref=" + STATUS_BRANCH)
            previous = json.loads(base64.b64decode(item["content"]))
            sha = item["sha"]
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise
        if previous.get("run_number", 0) > report["run_number"]:
            print("A newer push has already published its result.")
            return
        if report["status"] == "passed":
            report["last_verified_at"] = report["checked_at"]
            report["last_verified_support_sha256"] = report["support_sha256"]
        else:
            report["last_verified_at"] = previous.get("last_verified_at")
            report["last_verified_support_sha256"] = previous.get("last_verified_support_sha256")
        body = {"branch": STATUS_BRANCH, "message": "Update hotline verification result [skip ci]", "content": base64.b64encode((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode()).decode()}
        if sha:
            body["sha"] = sha
        try:
            github("PUT", "/contents/status.json", body)
            return
        except urllib.error.HTTPError as exc:
            if exc.code != 409 or attempt == 2:
                raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", default="index.html")
    parser.add_argument("--report", default="hotline-check-report.json")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    try:
        report = verify(args.index)
    except Exception as exc:
        report = {"status": "unavailable", "issues": [str(exc)], "checks": []}
        try:
            support, _ = read_support(args.index)
            report["support_sha256"] = hashlib.sha256(support.encode()).hexdigest()
        except Exception:
            pass
    report.update({"schema_version": 1, "source": DIRECTORY, "scope": "Names, telephone numbers, official website links and opening hours published in the directory profiles. HOPE hours are not published there and are not automatically verified.", "checked_at": datetime.now(timezone.utc).isoformat(), "source_sha": os.environ.get("GITHUB_SHA", "local"), "run_number": int(os.environ.get("GITHUB_RUN_NUMBER", "0")), "run_url": "https://github.com/" + os.environ.get("GITHUB_REPOSITORY", "Anbu47/W4GZ-Trust-and-Hope") + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "0")})
    if args.publish:
        try:
            publish(report)
        except Exception as exc:
            report["issues"].append("Cannot publish verification result: " + str(exc))
            report["status"] = "unavailable"
    Path(args.report).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = "## Find A Helpline contact check\n\nResult: **" + report["status"] + "**\n\n" + "\n".join("- " + issue for issue in report["issues"]) + "\n\n" + report["scope"] + "\n"
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as file:
            file.write(summary)
    print(summary)
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
