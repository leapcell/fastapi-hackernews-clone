from fastapi import FastAPI, Depends, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import urllib.parse
from models import Post, Comment, get_db, check_and_update_tables
from datetime import datetime

# Initialize a FastAPI application
app = FastAPI()

# Set up Jinja2 templates with the specified directory
templates = Jinja2Templates(directory="templates")


# Home page route, returns an HTML response
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # Get a database session
    db = get_db()
    if not db:
        # Return a template page indicating missing PostgreSQL connection
        return templates.TemplateResponse("missing-pg.html", {"request": request})
    # Check and update database tables
    check_and_update_tables()
    # Query all posts and sort them by creation time in descending order
    posts = db.query(Post).order_by(Post.created_at.desc()).all()
    # Process post data
    posts = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "link": post.link,
            # Extract hostname from the link if available
            "host": urllib.parse.urlparse(post.link).hostname if post.link else None,
            # Count comments for each post
            "comment_count": db.query(Comment)
            .filter(Comment.post_id == post.id)
            .count(),
        }
        for post in posts
    ]
    # Render the index page with processed post data
    return templates.TemplateResponse(
        "index.html", {"request": request, "posts": posts}
    )


# Route to create a new post, handles POST requests
@app.post("/new")
def new_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    link: str = Form(...),
):
    # Get a database session
    db = get_db()
    if not db:
        # Redirect to the home page if database connection fails
        return RedirectResponse(url="/", status_code=303)
    # Create a new post object
    new_post = Post(title=title, content=content, link=link)
    # Add the new post to the database session
    db.add(new_post)
    # Commit changes to the database
    db.commit()
    # Refresh the new post object
    db.refresh(new_post)
    # Redirect to the home page
    return RedirectResponse(url="/", status_code=303)


# Route to view a single post's details, returns an HTML response
@app.get("/post/{post_id}", response_class=HTMLResponse)
def post_detail(request: Request, post_id: int):
    # Get a database session
    db = get_db()
    if not db:
        # Redirect to the home page if database connection fails
        return RedirectResponse(url="/", status_code=303)
    # Query the post by its ID
    post = db.query(Post).filter(Post.id == post_id).first()
    # Render the post detail page with post and comment data
    return templates.TemplateResponse(
        "post_detail.html",
        {
            "request": request,
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": post.created_at,
                "link": post.link,
                # Extract hostname from the link if available
                "host": (
                    urllib.parse.urlparse(post.link).hostname if post.link else None
                ),
                "comments": [
                    {
                        "id": comment.id,
                        "content": comment.content,
                        "created_at": comment.created_at,
                    }
                    for comment in post.comments
                ],
            },
        },
    )


# Route to add a comment to a post, handles POST requests
@app.post("/post/{post_id}/comment")
def add_comment(post_id: int, content: str = Form(...)):
    # Get a database session
    db = get_db()
    if not db:
        # Redirect to the home page if database connection fails
        return RedirectResponse(url="/", status_code=303)
    # Query the post by its ID
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        # Create a new comment object
        comment = Comment(content=content, post=post)
        # Add the new comment to the database session
        db.add(comment)
        # Commit changes to the database
        db.commit()
        # Refresh the new comment object
        db.refresh(comment)
        # Redirect to the post detail page
        return RedirectResponse(url=f"/post/{post_id}", status_code=303)
    # Redirect to the home page if the post is not found
    return RedirectResponse(url="/", status_code=303)
