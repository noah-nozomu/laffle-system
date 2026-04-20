from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order_completed_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='会計完了日時'),
        ),
    ]
