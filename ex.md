# DRY — Don't Repeat Yourself
```python
article.author.first_name + " " + article.author.last_name

article.author.first_name + " " + article.author.last_name

article.author.first_name + " " + article.author.last_name
article.author.first_name + " " + article.author.last_name
```

```python
def full_name(user):
    return f"{user.first_name} {user.last_name}"
```
full_name(user)
full_name(user)
full_name(user)
full_name(user)

# KISS — Keep It Simple, Stupid

Погано:

```python
CommentFactoryBuilderManager(...)
```

Добре:

```python
Comment.objects.create(...)
```

# Boy Scout Rule
> Завжди залишайте код трохи чистішим, ніж він був до вас.

# Git Workflow

# Хороші коміти

# Хороший Pull Request

* короткий опис виконаної роботи;
* посилання на задачу в Jira;
* список змін;
* інформацію про міграції;
* інструкцію, як перевірити функціональність;
* за потреби — скріншоти інтерфейсу до та після змін.

# Навіщо потрібен Code Review

* знайти потенційні баги;
* перевірити відповідність архітектурі проєкту;
* переконатися, що новий код читається так само легко, як і старий;
* запобігти дублюванню функціональності;
* навчити менш досвідчених розробників;
* поширити знання про новий функціонал серед команди.