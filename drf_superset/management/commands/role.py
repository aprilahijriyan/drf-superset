import sys
from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser

from ...models import Permission, Role


class Command(BaseCommand):
    help = "Role Management"

    def add_arguments(self, parser: CommandParser) -> None:
        subparsers = parser.add_subparsers(dest="sub")
        new_parser = subparsers.add_parser("new", help="Create role")
        new_parser.add_argument("name")
        remove_parser = subparsers.add_parser("remove", help="Remove role")
        remove_parser.add_argument("name", help="Role name")
        update_parser = subparsers.add_parser("update", help="Update role")
        update_parser.add_argument("name")
        subparsers.add_parser("list", help="List roles")
        subparsers.add_parser("drop", help="Drop roles")

    def handle_new(self, *args: Any, **options: Any) -> Optional[str]:
        name = options["name"]
        role = Role.objects.filter(name=name).first()
        if role:
            self.stdout.write(self.style.ERROR(f"Role {name!r} already exist"))
        else:
            description = input("Role description: ")
            if description:
                role = Role.objects.create(name=name, description=description)
                permissions = input("Role permissions (separated by commas): ").split(
                    ","
                )
                for p in permissions:
                    p = p.strip()
                    p = Permission.objects.filter(name=p).first()
                    if p:
                        role.permissions.add(p)
                        self.stdout.write(
                            self.style.SUCCESS(f"+ Adding {p.name!r} permission")
                        )

                self.stdout.write(self.style.SUCCESS(f"Role {name!r} created"))
            else:
                self.stdout.write(self.style.ERROR("Role description is required"))

    def handle_remove(self, *args: Any, **options: Any) -> Optional[str]:
        name = options["name"]
        role = Role.objects.filter(name=name).first()
        if role:
            role.delete()
            self.stdout.write(self.style.SUCCESS(f"Role {name!r} deleted"))
        else:
            self.stdout.write(self.style.ERROR(f"Role {name!r} not found"))

    def handle_update(self, *args: Any, **options: Any) -> Optional[str]:
        name = options["name"]
        role = Role.objects.filter(name=name).first()
        if role:
            name = input("New role name: ")
            if name:
                role.name = name

            description = input("New role description: ")
            if description:
                role.description = description

            role.save()
            self.stdout.write(self.style.SUCCESS(f"Role {name!r} updated"))
        else:
            self.stdout.write(self.style.ERROR(f"Role {name!r} not found"))

    def handle_list(self, *args: Any, **options: Any) -> Optional[str]:
        roles = Role.objects.all()
        self.stdout.write(self.style.WARNING(f"Total roles: {len(roles)}"))
        for r in roles:
            perms = ", ".join([perm.name for perm in r.permissions.all()])
            self.stdout.write(
                self.style.SUCCESS(f"* {r.name} - {r.description} [{perms}]")
            )

    def handle_drop(self, *args: Any, **options: Any) -> Optional[str]:
        Role.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Dropping role is complete"))

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        subcommand = options["sub"]
        if subcommand is None:
            self.print_help(sys.argv[0], "role")
            return

        handle = getattr(self, f"handle_{subcommand}")
        handle(*args, **options)
