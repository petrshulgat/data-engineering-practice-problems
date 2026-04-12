import requests
import csv
import json
from pathlib import Path 

posts_url = 'https://jsonplaceholder.typicode.com/posts'
Fieldnames = ['post_id', 'post_title', 'comment_id', 'commenter_email', 'comment_body']

def main():

    response = requests.get(posts_url)
    response.raise_for_status()
    posts = response.json()

    filename = Path('posts_with_comments.csv')
    count = 0

    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=Fieldnames)
        writer.writeheader()

        for post in posts:
            comments_url = f'https://jsonplaceholder.typicode.com/posts/{post["id"]}/comments'

            comment_response = requests.get(comments_url)
            comment_response.raise_for_status()
            comments = comment_response.json()

            for comment in comments:
                writer.writerow({
                    'post_id': post['id'],
                    'post_title': post['title'],
                    'comment_id': comment['id'],
                    'commenter_email': comment['email'],
                    'comment_body': comment['body']
                })
                count += 1

        print(count)


if __name__ == '__main__':
    main()
            
        