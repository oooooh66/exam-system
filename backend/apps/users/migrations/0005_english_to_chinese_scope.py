# Data migration – convert business_scope values from English to Chinese
from django.db import migrations

SQL_FORWARD = """
    UPDATE busi_users SET business_scope = '["资产"]'
    WHERE JSON_CONTAINS(business_scope, '"asset"')
      AND NOT JSON_CONTAINS(business_scope, '"liability"')
      AND NOT JSON_CONTAINS(business_scope, '"retail"');

    UPDATE busi_users SET business_scope = '["负债"]'
    WHERE JSON_CONTAINS(business_scope, '"liability"')
      AND NOT JSON_CONTAINS(business_scope, '"asset"')
      AND NOT JSON_CONTAINS(business_scope, '"retail"');

    UPDATE busi_users SET business_scope = '["资产","负债"]'
    WHERE JSON_CONTAINS(business_scope, '"asset"')
      AND JSON_CONTAINS(business_scope, '"liability"');

    UPDATE busi_users SET business_scope = '["零售"]'
    WHERE JSON_CONTAINS(business_scope, '"retail"');
"""

SQL_REVERSE = """
    UPDATE busi_users SET business_scope = '["asset"]'
    WHERE JSON_CONTAINS(business_scope, '"资产"')
      AND NOT JSON_CONTAINS(business_scope, '"负债"');

    UPDATE busi_users SET business_scope = '["liability"]'
    WHERE JSON_CONTAINS(business_scope, '"负债"')
      AND NOT JSON_CONTAINS(business_scope, '"资产"');

    UPDATE busi_users SET business_scope = '["asset","liability"]'
    WHERE JSON_CONTAINS(business_scope, '"资产"')
      AND JSON_CONTAINS(business_scope, '"负债"');
"""


class Migration(migrations.Migration):
    dependencies = [('users', '0004_convert_business_scope_to_json')]
    operations = [migrations.RunSQL(SQL_FORWARD, SQL_REVERSE)]
