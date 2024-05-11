#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management.base import BaseCommand

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

class Command(BaseCommand):
    help = 'Удаление публикаций'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Подтвердить удаление без запроса подтверждения'
        )

    def handle(self, *args, **options):
        # Импортируем модели только когда это необходимо, внутри метода
        from news.models import Post, Category

        if not options['yes']:
            answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no: ')
            if answer != 'yes':
                self.stdout.write(self.style.ERROR('Отменено'))
                return

        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(
                f'Успешно удалены все новости из категории {category.name}'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категория "{options["category"]}" не существует'))

if __name__ == '__main__':
    main()
