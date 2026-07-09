"""
初始化数据管理命令

创建默认角色用户：
- admin / admin123 （管理员）
- teacher / teacher123 （教师）
- student / student123 （学生）

使用方法：
    python manage.py init_data
"""
from django.core.management.base import BaseCommand
from apps.users.models import BusiUser


class Command(BaseCommand):
    help = '初始化默认用户数据'

    def handle(self, *args, **options):
        # 创建管理员
        admin, created = BusiUser.objects.get_or_create(
            username='admin',
            defaults={'role': 'admin', 'is_staff': True, 'is_superuser': True},
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('管理员创建成功 (admin / admin123)'))
        else:
            self.stdout.write(self.style.WARNING('管理员已存在，跳过'))

        # 创建教师
        teacher, created = BusiUser.objects.get_or_create(
            username='teacher',
            defaults={'role': 'teacher'},
        )
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            self.stdout.write(self.style.SUCCESS('教师创建成功 (teacher / teacher123)'))
        else:
            self.stdout.write(self.style.WARNING('教师已存在，跳过'))

        # 创建学生
        student, created = BusiUser.objects.get_or_create(
            username='student',
            defaults={'role': 'student'},
        )
        if created:
            student.set_password('student123')
            student.save()
            self.stdout.write(self.style.SUCCESS('学生创建成功 (student / student123)'))
        else:
            self.stdout.write(self.style.WARNING('学生已存在，跳过'))

        self.stdout.write(self.style.SUCCESS('\n初始化完成！'))
