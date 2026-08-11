# Switch to ChineseJSONField (backed by MySQL patch in utils.apps)
import utils.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_busiuser_org_no'),
        ('exams', '0008_alter_busiexamsession_exam_scope'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busiuser',
            name='business_scope',
            field=utils.fields.ChineseJSONField(blank=True, default=list, verbose_name='分管业务'),
        ),
    ]
