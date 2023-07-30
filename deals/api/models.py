from django.db import models


class Gem(models.Model):
    """ Gem model """

    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Камень'
        verbose_name_plural = 'Камни'

    def __str__(self):
        return self.name


class Customer(models.Model):
    """ Customer model """

    username = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Имя пользователя'
    )
    gems = models.ManyToManyField(
        to=Gem,
        related_name='customers'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Deal(models.Model):
    """ Deal model """

    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.CASCADE,
        related_name='deals',
        verbose_name='Пользователь'
    )
    item = models.ForeignKey(
        to=Gem,
        on_delete=models.CASCADE,
        related_name='deals',
        verbose_name='Камень'
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество'
    )
    total = models.DecimalField(
        max_digits=9,
        decimal_places=2
    )
    date = models.DateTimeField(
        verbose_name='Дата и время создания'
    )

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return f'{self.customer.username} | {self.item.name}'
