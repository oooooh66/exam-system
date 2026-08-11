# Generated migration – add position and remark fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_busiuser_business_scope_busiuser_org_nm'),
    ]

    operations = [
        migrations.AddField(
            model_name='busiuser',
            name='position',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='岗位'),
        ),
        migrations.AddField(
            model_name='busiuser',
            name='remark',
            field=models.TextField(blank=True, default='', verbose_name='备注'),
        ),
    ]
