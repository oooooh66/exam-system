# Custom migration – convert business_scope from varchar to JSON array
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_add_position_remark'),
    ]

    operations = [
        # Step 1: widen the column so JSON arrays fit
        migrations.RunSQL(
            sql="ALTER TABLE busi_users MODIFY business_scope TEXT NOT NULL DEFAULT ('[]')",
            reverse_sql="ALTER TABLE busi_users MODIFY business_scope VARCHAR(20) NOT NULL DEFAULT ''",
        ),
        # Step 2: convert existing values into JSON arrays
        migrations.RunSQL(
            sql="""
                UPDATE busi_users SET business_scope = '[\"asset\"]'
                WHERE business_scope = 'asset';
                UPDATE busi_users SET business_scope = '[\"liability\"]'
                WHERE business_scope = 'liability';
                UPDATE busi_users SET business_scope = '[\"asset\",\"liability\"]'
                WHERE business_scope IN ('both');
                UPDATE busi_users SET business_scope = '[\"retail\"]'
                WHERE business_scope = 'retail';
                UPDATE busi_users SET business_scope = '[]'
                WHERE business_scope = '' OR business_scope IS NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Step 3: cast to JSON type
        migrations.RunSQL(
            sql="ALTER TABLE busi_users MODIFY business_scope JSON NOT NULL",
            reverse_sql="ALTER TABLE busi_users MODIFY business_scope VARCHAR(20) NOT NULL DEFAULT ''",
        ),
    ]
