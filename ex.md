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