from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse


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


@app.get("/api/posts", response_model=list[PostResponse])
def get_posts():
    return posts

@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "12 May, 2026",
    }
    posts.append(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=PostResponse)
def post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id")==post_id:
            title=post["title"] [:50]
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post,"title": title}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


## StarletteHTTPException Handler
@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )