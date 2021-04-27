import sys
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from ...models import Permission


class Command(BaseCommand):
    help = "Permission Management"

    def add_arguments(self, parser: CommandParser) -> None:
        subparsers = parser.add_subparsers(dest="sub")
        new_parser = subparsers.add_parser("new", help="Create permission")
        new_parser.add_argument("name")
        remove_parser = subparsers.add_parser("remove", help="Remove permission")
        remove_parser.add_argument("name", help="Permission name")
        update_parser = subparsers.add_parser("update", help="Update permission")
        update_parser.add_argument("name")
        subparsers.add_parser("list", help="List permissions")
        subparsers.add_parser("drop", help="Drop permissions")

    def handle_new(self, *args: Any, **options: Any) -> Optional[str]:
        name = options["name"]
        permission = Permission.objects.filter(name=name).first()
        if permission:
            self.stdout.write(self.style.ERROR(f"Permission {name!r} already exist"))
        else:
            description = input("Permission description: ")
            if description:
                Permission.objects.create(name=name, description=description)
                self.stdout.write(self.style.SUCCESS(f"Permission {name!r} created"))
            else:
                self.stdout.write(
                    self.style.ERROR("Permission description is required")
                )

    def handle_remove(self, *args: Any, **options: Any) -> Optional[str]:
        name = options["name"]
        permission = Permission.objects.filter(name=name).first()
        if permission:
            permission.delete()
            self.stdout.write(self.style.SUCCESS(f"Permission {name!r} deleted"))
        else:
            self.stdout.write(self.style.ERROR(f"Permission {name!r} not found"))

    def handle_update(self, *args: Any, **options: Any) -> Optional[str]:
        name = options["name"]
        permission = Permission.objects.filter(name=name).first()
        if permission:
            name = input("New permission name: ")
            if name:
                permission.name = name

            description = input("New permission description: ")
            if description:
                permission.description = description

            permission.save()
            self.stdout.write(self.style.SUCCESS(f"Permission {name!r} updated"))
        else:
            self.stdout.write(self.style.ERROR(f"Permission {name!r} not found"))

    def handle_list(self, *args: Any, **options: Any) -> Optional[str]:
        permissions = Permission.objects.all()
        self.stdout.write(self.style.WARNING(f"Total permissions: {len(permissions)}"))
        for r in permissions:
            self.stdout.write(self.style.SUCCESS(f"* {r.name} - {r.description}"))

    def handle_drop(self, *args: Any, **options: Any) -> Optional[str]:
        Permission.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Dropping permission is complete"))

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        subcommand = options["sub"]
        if subcommand is None:
            self.print_help(sys.argv[0], "permission")
            return

        handle = getattr(self, f"handle_{subcommand}")
        handle(*args, **options)
