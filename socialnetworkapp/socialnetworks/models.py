from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField

# Create your models here.


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)


class Category(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=100, null=False)
    description = RichTextField(null=True)
    image = models.ImageField(upload_to="products/%Y/%m")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_query_name='product')

    def __str__(self):
        return self.name


class Auction(models.Model):
    content = RichTextField(null=True)
    starting_price = models.FloatField(null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    date_of_payment = models.DateField(null=True)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    owner = models.ForeignKey(User, related_name='user_of', on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)
    user_care = models.ManyToManyField(User, related_query_name='auction')


class ParticipateAuction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_query_name="participateauction")
    price = models.FloatField(null=True)


class Post(BaseModel):
    content = RichTextField(null=True)
    image = models.ImageField(upload_to="posts/%Y/%m")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_hashtag = models.ManyToManyField('Hashtag')


class ReportType(BaseModel):
    content = RichTextField(null=True)

    def __str__(self):
        return self.content


class Report(BaseModel):
    reason = RichTextField(null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE)


class Notice(BaseModel):
    content = RichTextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Hashtag(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class LikeType(BaseModel):
    name = models.CharField(max_length=100, null=False)
    icon = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Like(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_type = models.ForeignKey(LikeType, on_delete=models.CASCADE)


class Comments(BaseModel):
    content = RichTextField(null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE)



