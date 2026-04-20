from django.db import migrations, models


def set_display_order(apps, schema_editor):
    Product = apps.get_model('store', 'Product')
    for index, product in enumerate(Product.objects.order_by('id'), start=1):
        product.display_order = index
        product.save(update_fields=['display_order'])


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_orderitem_temperature_product_temperature_option'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='display_order',
            field=models.PositiveIntegerField(db_index=True, default=0, verbose_name='表示順'),
        ),
        migrations.RunPython(set_display_order, migrations.RunPython.noop),
    ]
