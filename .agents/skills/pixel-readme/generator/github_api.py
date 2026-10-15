"""
GitHub API Integration for Pixel Readme Kit
Fetches live repository stats, user profiles, and star trajectories
using pure standard library urllib (zero external dependencies).
"""

import json
import os
import re
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List, Tuple


def _get_auth_token(token: Optional[str] = None) -> Optional[str]:
    """Resolves GitHub token from parameter or standard environment variables."""
    if token:
        return token
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def _github_request(url: str, token: Optional[str] = None, accept: str = "application/vnd.github.v3+json") -> Tuple[Optional[Any], Optional[str]]:
    """
    Performs an authenticated or unauthenticated GET request to GitHub API.
    Returns (data, error_message).
    """
    headers = {
        "User-Agent": "pixel-readme-kit/5.0",
        "Accept": accept,
    }
    resolved_token = _get_auth_token(token)
    if resolved_token:
        headers["Authorization"] = f"Bearer {resolved_token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw), None
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, f"Resource not found (404): {url}"
        elif e.code == 403:
            return None, "GitHub API rate limit exceeded (403). Set GITHUB_TOKEN environment variable."
        return None, f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def fetch_repo_data(repo: str, token: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Fetches public repository statistics from GitHub API.
    repo format: "owner/repo"
    """
    repo = repo.strip().strip("/")
    if not repo or "/" not in repo:
        return None, f"Invalid repository format '{repo}'. Expected 'owner/repo'."

    url = f"https://api.github.com/repos/{repo}"
    data, err = _github_request(url, token)
    if err or not isinstance(data, dict):
        return None, err

    result = {
        "repo": data.get("full_name", repo),
        "name": data.get("name", ""),
        "owner": data.get("owner", {}).get("login", ""),
        "description": data.get("description") or "",
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "watchers": data.get("subscribers_count", data.get("watchers_count", 0)),
        "open_issues": data.get("open_issues_count", 0),
        "license": (data.get("license") or {}).get("spdx_id", "MIT"),
        "language": data.get("language") or "Python",
        "archived": data.get("archived", False),
    }
    return result, None


def fetch_user_data(username: str, token: Optional[str] = None) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Fetches public user profile information from GitHub API.
    """
    user = username.strip().lstrip("@")
    if not user:
        return None, "Empty username provided."

    url = f"https://api.github.com/users/{user}"
    data, err = _github_request(url, token)
    if err or not isinstance(data, dict):
        return None, err

    result = {
        "username": data.get("login", user),
        "name": data.get("name") or user,
        "bio": data.get("bio") or "Building high-performance software and systems.",
        "company": data.get("company") or "",
        "location": data.get("location") or "REMOTE // UTC",
        "public_repos": data.get("public_repos", 0),
        "followers": data.get("followers", 0),
        "following": data.get("following", 0),
        "avatar_url": data.get("avatar_url", ""),
        "blog": data.get("blog", ""),
    }
    return result, None


def fetch_star_trajectory(repo: str, token: Optional[str] = None, sample_count: int = 6) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Computes or estimates star growth trajectory for starchart.
    If full stargazer history cannot be fetched due to API limits,
    gracefully interpolates a realistic logarithmic curve based on current stargazers.
    """
    repo_data, err = fetch_repo_data(repo, token)
    if err or not repo_data:
        # Fallback trajectory if network failed
        return {
            "repo": repo,
            "points": [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0],
            "current": "1,650",
            "delta": "+78% past 6m",
            "error": err
        }, err

    total_stars = repo_data["stars"]
    cur_str = f"{total_stars:,}"

    if total_stars <= 0:
        return {
            "repo": repo_data["repo"],
            "points": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "current": "0",
            "delta": "0% past 6m",
            "stars": 0,
            "forks": repo_data["forks"],
            "watchers": repo_data["watchers"]
        }, None

    # Try fetching star timestamps with custom header
    stargazers_url = f"https://api.github.com/repos/{repo}/stargazers?per_page=100"
    stargazers_data, star_err = _github_request(stargazers_url, token, accept="application/vnd.github.v3.star+json")

    points: List[float] = []

    if isinstance(stargazers_data, list) and len(stargazers_data) > 5 and total_stars <= 100:
        # We have the full star list for small repo!
        step = max(1, len(stargazers_data) // (sample_count - 1))
        sampled = [stargazers_data[i] for i in range(0, len(stargazers_data), step)][:sample_count - 1]
        points = [float(i + 1) for i in range(len(sampled))]
        points.append(float(total_stars))
        while len(points) < sample_count:
            points.insert(0, 0.0)
    else:
        # Interpolate a natural logarithmic/S-curve growth trajectory up to current stars
        curve_weights = [0.08, 0.18, 0.35, 0.58, 0.82, 1.0]
        points = [round(total_stars * w, 1) for w in curve_weights]

    first_val = points[0] if points else 1.0
    if first_val > 0:
        pct = int(((total_stars - first_val) / first_val) * 100)
        delta_str = f"+{pct}% past 6m" if pct > 0 else "0% past 6m"
    else:
        delta_str = "+100% past 6m"

    return {
        "repo": repo_data["repo"],
        "points": points,
        "current": cur_str,
        "delta": delta_str,
        "stars": total_stars,
        "forks": repo_data["forks"],
        "watchers": repo_data["watchers"]
    }, None


_GITHUB_CACHE: Dict[Tuple[str, str], Tuple[str, str]] = {}


def format_count(n: Any) -> str:
    """Formats numeric count with K/M suffixes."""
    if n is None:
        return "--"
    try:
        n = int(n)
    except (ValueError, TypeError):
        return str(n)
    if n >= 1000000:
        return f"{n/1000000:.1f}M"
    if n >= 1000:
        return f"{n/1000:.1f}k"
    return str(n)


def fetch_github_stat(repo: str, stat_type: str, auto_fetch: bool = True) -> Tuple[str, str]:
    """
    Fetches specific stat for a chip or badge from GitHub API.
    Returns (display_text, link_url).
    Caches only successful network responses.
    """
    clean_repo = repo.strip().strip("/") if repo else "Kazinagg/readme-kit"
    st = stat_type.lower()
    cache_key = (clean_repo, st)

    def_links = {
        "stars": f"https://github.com/{clean_repo}/stargazers",
        "forks": f"https://github.com/{clean_repo}/network/members",
        "issues": f"https://github.com/{clean_repo}/issues",
        "watchers": f"https://github.com/{clean_repo}/watchers",
        "version": f"https://github.com/{clean_repo}/releases",
        "release": f"https://github.com/{clean_repo}/releases",
        "license": f"https://github.com/{clean_repo}",
    }
    def_link = def_links.get(st, f"https://github.com/{clean_repo}")

    fallback_texts = {
        "stars": "★ STARS",
        "forks": "FORKS",
        "issues": "● ISSUES",
        "license": "LICENSE: MIT",
        "version": "v1.0.0",
        "release": "v1.0.0",
        "watchers": "WATCHERS",
    }
    fallback_text = fallback_texts.get(st, st.upper())

    if not auto_fetch:
        return (fallback_text, def_link)

    if cache_key in _GITHUB_CACHE:
        return _GITHUB_CACHE[cache_key]

    try:
        if st in ("version", "release"):
            url = f"https://api.github.com/repos/{clean_repo}/releases/latest"
            data, err = _github_request(url)
            if data and isinstance(data, dict):
                tag = data.get("tag_name") or data.get("name") or "v1.0"
                res = (str(tag), def_link)
                _GITHUB_CACHE[cache_key] = res
                return res
        else:
            rdata, err = fetch_repo_data(clean_repo)
            if rdata and isinstance(rdata, dict):
                if st == "stars":
                    count = format_count(rdata.get("stars", 0))
                    res = (f"★ {count}", def_link)
                elif st == "forks":
                    count = format_count(rdata.get("forks", 0))
                    res = (f"FORKS: {count}", def_link)
                elif st == "issues":
                    count = format_count(rdata.get("open_issues", 0))
                    res = (f"● ISSUES: {count}", def_link)
                elif st == "watchers":
                    count = format_count(rdata.get("watchers", 0))
                    res = (f"WATCHERS: {count}", def_link)
                elif st == "license":
                    lic = rdata.get("license") or "MIT"
                    res = (f"LICENSE: {lic}", def_link)
                else:
                    res = (f"{st.upper()}", def_link)

                _GITHUB_CACHE[cache_key] = res
                return res
    except Exception:
        pass

    return (fallback_text, def_link)

