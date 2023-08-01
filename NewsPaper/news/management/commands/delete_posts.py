from django.core.management.base import BaseCommand, CommandError
from ...models import Post, Category


class Command(BaseCommand):
    help = 'Удаляет посты выбранной вами категории. В аргументы передайте название категории, в случае если вы хотите удалить все посты введите "all" '  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True  # напоминать ли о миграциях. Если true — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('argument', type=str)

    def handle(self, *args, **options):
        # здесь можете писать любой код, который выполнится при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all post? yes/no')  # спрашиваем пользователя, действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':  # в случае подтверждения действительно удаляем все товары

            if options['argument'] == 'all':
                Post.objects.all().delete()
            elif options['argument'] == 'спорт':
                Post.objects.filter(post_category__category_name='спорт').delete()
            elif options['argument'] == 'политика':
                Post.objects.filter(post_category__category_name='политика').delete()
            elif options['argument'] == 'образование':
                Post.objects.filter(post_category__category_name='образование').delete()
            elif options['argument'] == 'медицина':
                Post.objects.filter(post_category__category_name='медицина').delete()
            else:
                raise CommandError('Такой категории не существует')

            self.stdout.write(self.style.SUCCESS('Выбранные посты в категории успешно удалены!'))
            return

        self.stdout.write(
            self.style.ERROR('Access denied'))  # в случае неправильного подтверждения, говорим, что в доступе отказано