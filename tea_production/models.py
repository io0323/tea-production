from django.db import models
from django.utils import timezone

class Production(models.Model):
    """
    茶葉の生産データを管理するモデル
    """
    TEA_TYPES = [
        ('煎茶', '煎茶'),
        ('玉露', '玉露'),
        ('抹茶', '抹茶'),
        ('ほうじ茶', 'ほうじ茶'),
    ]
    
    QUALITY_GRADES = [
        ('A級', 'A級'),
        ('B級', 'B級'),
        ('C級', 'C級'),
    ]
    
    tea_type = models.CharField('茶葉の種類', max_length=50, choices=TEA_TYPES)
    production_date = models.DateField('生産日')
    quantity = models.DecimalField('生産量(kg)', max_digits=10, decimal_places=2)
    quality_check = models.CharField('品質評価', max_length=50, choices=QUALITY_GRADES)
    quality_notes = models.TextField('品質メモ', blank=True, null=True)
    created_at = models.DateTimeField('登録日時', default=timezone.now)

    class Meta:
        verbose_name = '生産データ'
        verbose_name_plural = '生産データ'
        ordering = ['-production_date']

    def __str__(self):
        return f"{self.production_date} - {self.tea_type} ({self.quantity}kg)"

class Shipment(models.Model):
    """
    出荷データを管理するモデル
    """
    production = models.ForeignKey(
        Production,
        on_delete=models.PROTECT,
        verbose_name='生産データ'
    )
    shipment_date = models.DateField('出荷日')
    quantity = models.DecimalField('出荷量(kg)', max_digits=10, decimal_places=2)
    customer_name = models.CharField('顧客名', max_length=100)
    customer_contact = models.CharField('連絡先', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('登録日時', default=timezone.now)

    class Meta:
        verbose_name = '出荷データ'
        verbose_name_plural = '出荷データ'
        ordering = ['-shipment_date']

    def __str__(self):
        return f"{self.shipment_date} - {self.customer_name} ({self.quantity}kg)"

class Inventory(models.Model):
    """
    在庫データを管理するモデル
    """
    production = models.OneToOneField(
        Production,
        on_delete=models.PROTECT,
        verbose_name='生産データ'
    )
    quantity = models.DecimalField('在庫量(kg)', max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField('最終更新', auto_now=True)

    class Meta:
        verbose_name = '在庫データ'
        verbose_name_plural = '在庫データ'
        ordering = ['-last_updated']

    def __str__(self):
        return f"{self.production.tea_type} - {self.quantity}kg" 