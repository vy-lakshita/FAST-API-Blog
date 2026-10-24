from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException, status

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] =[
{
    "id": 1,
    "author" :"Isaac Asminov",
    "title": "The begining and the end",
    "content": "About universe and its working",
    "Date" : "12 Aug, 1977"
},
{
    "id": 2,
    "author" :"Jane Austen",
    "title": "Little Women",
    "content": "About women",
    "Date" : "12 Oct, 1977"

}
]

@app.get("/",include_in_schema=False)
@app.get("/posts",include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse(request,
                                      "home.html", 
                                      {"posts": posts, "title": "Home"},)


@app.get("/api/posts")
def get_posts():
    return posts



@app.get("/api/posts/{post_id}")
def get_post(request: Request, post_id: int):
    for post in posts:
        if post.get("id")==post_id:
            title=post["title"] [:50]
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post,"title": title}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


