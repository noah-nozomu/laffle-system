from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_display_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['display_order', 'id']},
        ),
    ]
