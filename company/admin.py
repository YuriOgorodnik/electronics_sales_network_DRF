from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from company.models import Company, Product


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Company
    """

    list_display = (
        "name",
        "email",
        "country",
        "city",
        "supplier_link",
        "debt",
        "created_at",
    )
    list_filter = ("city",)
    search_fields = ("name", "city")
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        """
        Создает ссылку на страницу редактирования поставщика
        """
        if obj.supplier:
            url = reverse("admin:company_company_change", args=[obj.supplier.pk])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "-"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        """
        Обнуляет задолженность выбранных компаний
        """
        queryset.update(debt=0)

    clear_debt.short_description = "Очистить задолженность"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для модели Product
    """

    list_display = ("name", "model", "release_date", "company")
    list_filter = ("company",)
    search_fields = ("name", "model")
