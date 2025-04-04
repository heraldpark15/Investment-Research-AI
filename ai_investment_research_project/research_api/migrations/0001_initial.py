# Generated by Django 5.1.7 on 2025-03-13 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="StockResearchData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ticker_symbol", models.CharField(db_index=True, max_length=10)),
                ("stock_price", models.FloatField(blank=True, null=True)),
                ("market_cap", models.CharField(blank=True, max_length=50)),
                ("pe_ratio", models.CharField(blank=True, max_length=20)),
                ("summary", models.TextField(blank=True)),
                ("research_timestamp", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name_plural": "Stock Research Data",
            },
        ),
    ]
