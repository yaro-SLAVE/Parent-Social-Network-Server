from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    logo = models.ImageField("Логотип", upload_to="images", null=True, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username

class Basement(models.Model):
    address = models.TextField("Адрес")
    capacity = models.IntegerField("Вместимость людей")

    def __str__(self) -> str:
        return self.address

class UserBasement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    basement = models.ForeignKey(Basement, on_delete=models.CASCADE)

class Child(models.Model):
    first_name = models.TextField("Имя")
    gender = models.TextField("Пол")
    birth_date = models.DateField("Дата рождения")
    basement = models.ForeignKey(Basement, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.first_name
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField("Заголовок")
    body = models.TextField("Тело поста")
    create_time = models.DateTimeField("Время опубликования")

    def __str__(self) -> str:
        return self.user + " " + self.title

class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.ImageField("Фото ребенка", upload_to="images")

    def __str__(self) -> str:
        return self.post.title + " " + self.post.user.username + " " + self.photo

class ChildPhoto(models.Model):
    photo = models.ForeignKey(PostPhoto, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField("Текст комментария")
    date = models.DateTimeField("Дата написания")

    def __str__(self) -> str:
        return self.user.username + " " + self.post.title + " " + self.date
    
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("Дата установки лайка", auto_now_add=True, blank=True)

class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("Дата установки лайка")

class Reaction(models.Model):
    reaction_name = models.TextField("Название реакции")
    reaction = models.TextField("Реакция её код")

    def __str__(self) -> str:
        return self.reaction_name

class PostReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE)
    date = models.DateTimeField("Дата установки реакции", auto_now_add=True, blank=True)