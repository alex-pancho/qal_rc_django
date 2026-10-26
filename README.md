# qal_rc_django
Try django

```text
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── app/
    ├── migrations/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    └── tests.py
```

```
Браузер: GET /posts/2/
   │
   ▼
Middleware (зверху вниз: сесії, безпека, наше логування…)
   │
   ▼
Головний urls.py ──include──► urls.py застосунку
   │   шукає перший маршрут, що підійшов: posts/<int:post_id>/
   ▼
View: post_detail(request, post_id=2)
   │   отримує дані, формує контекст
   ▼
render(request, "core/post.html", context)  ──► HTML
   │
   ▼
Middleware (знизу вгору)
   │
   ▼
Браузер отримує HTTP-відповідь (статус 200 + HTML)
```

```python
# --- urls
path("users/<str:username>/", views.user_profile, name="user_profile")
path("articles/<slug:article>/", views.article_detail, name="article_detail")
path("files/<uuid:file_id>/", views.download_file, name="download_file")
path("posts/<int:post_id>/", views.post_detail, name="post_detail")
# --- views
def user_profile(request, username):
    return render(request, "core/profile.html", {"username": username})

def article_detail(request, article):
    return render(request, "core/article.html", {"slug": article})

def download_file(request, file_id):
    return render(request, "core/download.html", {"file_id": file_id})

def post_detail(request, post_id):
    return render(request, "core/post.html", {"post_id": post_id})

def search(request):
    query = request.GET.get("q", "")       # /search/?q=django
    # query = request.GET.get("page", "")
    return render(request, "core/search.html", {"query": query})

```
```
	    Параметр шляху	Параметр запиту
Вигляд	/posts/5/	    /posts/?page=2&sort=new
```
```
Запит → Middleware 1 → Middleware 2 → Middleware 3 → View
Відповідь ← Middleware 1 ← Middleware 2 ← Middleware 3 ← View (Response)
```