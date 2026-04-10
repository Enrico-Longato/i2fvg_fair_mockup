from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("i2fvg_mockup", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyregistryheadquarters",
            name="tipo_impresa",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name="companyregistryfiltered",
            name="tipo_impresa",
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
