from typing import List, Dict, Any
from cf_api import Problem

def filter_problems(all_problems: List[Problem], filters: Dict[str, Any]) -> List[Problem]:
    """Filters the list of Problem objects based on user criteria."""
    min_rating = filters["min_rating"]
    max_rating = filters["max_rating"]
    selected_tags = filters["selected_tags"]
    limit = filters["limit"]

    filtered: List[Problem] = []
    for p in all_problems:
        p_rating = p.rating or 0
        
        # Filter by Rating
        if min_rating and p_rating < min_rating: continue
        if max_rating and p_rating > max_rating: continue
        
        # Filter by Tags (Matches ANY of the selected tags)
        # If no tags selected, it means ALL tags are accepted (matches CF behavior)
        if selected_tags and not any(t in p.tags for t in selected_tags):
            continue
            
        filtered.append(p)
        if len(filtered) >= limit:
            break

    return filtered
