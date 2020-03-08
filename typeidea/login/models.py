from django.db import models

# Create your models here.
class MyUser(models.Model):

    gener = (
        ('male','男'),
        ('female','女'),
    )

    name = models.CharField(max_length=50,verbose_name='用户名',unique=True)
    password = models.CharField(max_length=128,verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')
    create_time = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(max_length=30, choices=gener, verbose_name='性别')

    def print(self):
        print('print User Model')
        print(self.name)
        print(self.password)
        print(self.email)
        print(self.sex)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['create_time']
        verbose_name = verbose_name_plural = '用户'