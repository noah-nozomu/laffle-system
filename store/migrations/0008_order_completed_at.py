from django.db import migrations, models


def backfill_completed_at(apps, schema_editor):
    Order = apps.get_model('store', 'Order')
    Order.objects.filter(is_completed=True, completed_at__isnull=True).update(
        completed_at=models.F('created_at')
    )


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='completed_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='提供完了日時'),
        ),
        migrations.RunPython(backfill_completed_at, migrations.RunPython.noop),
    ]
