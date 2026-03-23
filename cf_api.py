from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import requests

@dataclass
class Problem:
    contestId: int
    index: str
    name: str
    rating: Optional[int]
    tags: List[str]

    @property
    def link(self) -> str:
        return f"https://codeforces.com/problemset/problem/{self.contestId}/{self.index}"

    @property
    def full_id(self) -> str:
        return f"{self.contestId}{self.index}"

def fetch_problems() -> List[Problem]:
    """Fetches and parses problems from Codeforces API into Problem objects."""
    url = "https://codeforces.com/api/problemset.problems"
    try:
        response = requests.get(url, timeout=10).json()
        if response.get("status") == "OK":
            problems_data = response["result"]["problems"]
            return [
                Problem(
                    contestId=p.get("contestId", 0),
                    index=p.get("index", ""),
                    name=p.get("name", "Unknown"),
                    rating=p.get("rating"),
                    tags=p.get("tags", [])
                )
                for p in problems_data
            ]
    except Exception as e:
        print(f"Error fetching data: {e}")
    return []
