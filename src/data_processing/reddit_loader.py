import praw
import json
import os
from datetime import datetime
from tqdm import tqdm
from config.settings import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT, DATA_RAW_PATH, SUBREDDIT_NAME

def scrape_subreddit(subreddit_name: str = SUBREDDIT_NAME, limit: int = 1000) -> str:
    """
    Scrape top posts and comments from a subreddit
    Returns path to the saved JSON file
    """
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    
    subreddit = reddit.subreddit(subreddit_name)
    dataset = []
    
    print(f"Scraping r/{subreddit_name}...")
    for post in tqdm(subreddit.top(limit=limit), total=limit):
        # Skip stickied posts (often rules/announcements)
        if post.stickied:
            continue
            
        post_data = {
            "id": post.id,
            "title": post.title,
            "text": post.selftext,
            "score": post.score,
            "url": post.url,
            "created_utc": post.created_utc,
            "num_comments": post.num_comments,
            "comments": []
        }
        
        # Fetch comments (skip MoreComments)
        post.comments.replace_more(limit=0)
        for comment in post.comments.list()[:100]:  # Limit to top 100 comments per post
            post_data["comments"].append({
                "id": comment.id,
                "body": comment.body,
                "score": comment.score
            })
        
        dataset.append(post_data)
    
    # Ensure output directory exists
    os.makedirs(DATA_RAW_PATH, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{subreddit_name}_{timestamp}.json"
    output_path = os.path.join(DATA_RAW_PATH, filename)
    
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Saved {len(dataset)} posts to {output_path}")
    return output_path

if __name__ == "__main__":
    scrape_subreddit()