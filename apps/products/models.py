from django.db import models
from django.utils.text import slugify


class Kategoriya(models.Model):
    nomi = models.CharField("Kategoriya nomi", max_length=255)
    slug = models.SlugField("URL manzili (Slug)", unique=True, blank=True)
    rasmi = models.ImageField("Kategoriya rasmi", upload_to='kategoriyalar/', blank=True, null=True)
    ota_kategoriya = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='bolalari', verbose_name="Ota kategoriya"
    )

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nomi.replace("'", ""))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nomi


class MashinaModeli(models.Model):
    brend = models.CharField("Marka (Chevrolet, Kia...)", max_length=100)
    nomi = models.CharField("Model nomi (Cobalt, Gentra...)", max_length=100)
    yil_boshlanishi = models.PositiveIntegerField("Ishlab chiqarilgan yili (dan)")
    yil_tugashi = models.PositiveIntegerField("Ishlab chiqarilgan yili (gacha)", null=True, blank=True)

    class Meta:
        verbose_name = "Avtomobil modeli"
        verbose_name_plural = "Avtomobil modellari"

    def __str__(self):
        oxirgi_yil = self.yil_tugashi if self.yil_tugashi else 'hozir'
        return f"{self.brend} {self.nomi} ({self.yil_boshlanishi}-{oxirgi_yil})"


class Mahsulot(models.Model):
    nomi = models.CharField("Ehtiyot qism nomi", max_length=255)
    slug = models.SlugField("URL manzili (Slug)", unique=True, blank=True)
    artikul_raqami = models.CharField("OEM / Artikul raqami", max_length=100, unique=True)

    kategoriya = models.ForeignKey(Kategoriya, on_delete=models.PROTECT, related_name='mahsulotlar',
                                   verbose_name="Kategoriya")
    mos_mashinalar = models.ManyToManyField(MashinaModeli, related_name='mos_detallar',
                                            verbose_name="Mos keladigan mashinalar")

    narxi = models.IntegerField("Narxi (so'm)")
    chegirmali_narxi = models.DecimalField("Chegirmadagi narxi", max_digits=10, decimal_places=2, null=True, blank=True)
    ombordagi_soni = models.PositiveIntegerField("Ombordagi soni (dona)", default=0)

    tavsifi = models.TextField("Batafsil tavsifi")
    faol = models.BooleanField("Sotuvda bormi?", default=True)
    qo_shilgan_sana = models.DateTimeField("Qo'shilgan sana", auto_now_add=True)
    rasm = models.ImageField(upload_to='mahsulotlar/', blank=True, null=True, verbose_name="Maxsulot rasmi")


    class Meta:
        verbose_name = "Ehtiyot qism"
        verbose_name_plural = "Ehtiyot qismlar"
        indexes = [models.Index(fields=['artikul_raqami', 'narxi'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            matn = f"{self.nomi}-{self.artikul_raqami}".replace("'", "")
            self.slug = slugify(matn)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nomi} (OEM: {self.artikul_raqami})"


class MahsulotRasmi(models.Model):
    mahsulot = models.ForeignKey(Mahsulot, on_delete=models.CASCADE, related_name='rasmlari', verbose_name="Mahsulot")
    rasm = models.ImageField("Mahsulot rasmi", upload_to='mahsulotlar/')
    asosiy_rasm = models.BooleanField("Asosiy rasmmi?", default=False)

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"

    def __str__(self):
        return f"Rasm: {self.mahsulot.nomi}"
