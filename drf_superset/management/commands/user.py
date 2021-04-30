import sys
from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone

from ...core.helpers import generate_random_string
from ...models import Role


class Command(BaseCommand):
    help = "User Management"

    def add_arguments(self, parser: CommandParser) -> None:
        subparsers = parser.add_subparsers(dest="sub")
        new_parser = subparsers.add_parser("new", help="Create user")
        new_parser.add_argument("email")
        remove_parser = subparsers.add_parser("remove", help="Remove user")
        remove_parser.add_argument("email", help="User email")
        update_parser = subparsers.add_parser("update", help="Update user")
        update_parser.add_argument("email")
        subparsers.add_parser("list", help="List users")
        subparsers.add_parser("drop", help="Drop users")

    def handle_new(self, *args: Any, **options: Any) -> Optional[str]:
        email = options["email"]
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        if user:
            self.stdout.write(self.style.ERROR(f"User {email!r} already exist"))
        else:
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            password = input("Password: ").strip()

            if not first_name:
                self.stdout.write(self.style.ERROR("First name required"))
                exit(1)

            if not last_name:
                self.stdout.write(self.style.ERROR("Last name required"))
                exit(1)

            if not password:
                self.stdout.write(self.style.ERROR("Password required"))
                exit(1)

            fullname = first_name + " " + last_name
            username = fullname.replace(" ", "") + generate_random_string(4)
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                fullname=fullname,
                username=username,
                email=email,
                confirmed=True,
                confirmed_date=timezone.now(),
            )
            user.set_password(password)
            user.save()
            roles = input("User roles (separated by commas): ").split(",")
            for p in roles:
                p = p.strip()
                p = Role.objects.filter(name=p).first()
                if p:
                    user.roles.add(p)
                    self.stdout.write(self.style.SUCCESS(f"+ Adding {p.name!r} role"))

            self.stdout.write(self.style.SUCCESS(f"User {email!r} created"))

    def handle_remove(self, *args: Any, **options: Any) -> Optional[str]:
        email = options["email"]
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        if user:
            user.delete()
            self.stdout.write(self.style.SUCCESS(f"User {email!r} deleted"))
        else:
            self.stdout.write(self.style.ERROR(f"User {email!r} not found"))

    def handle_update(self, *args: Any, **options: Any) -> Optional[str]:
        email = options["email"]
        User = get_user_model()
        user = User.objects.filter(email=email).first()
        if user:
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            if first_name:
                user.first_name = first_name
            else:
                first_name = user.first_name

            if last_name:
                user.last_name = last_name
            else:
                last_name = user.last_name

            fullname = first_name + " " + last_name
            if fullname != user.fullname:
                username = fullname.replace(" ", "") + generate_random_string(4)
                user.fullname = fullname
                user.username = username

            roles = []
            for p in input("User roles (separated by commas): ").split(","):
                p = p.strip()
                p = Role.objects.filter(name=p).first()
                if p:
                    roles.append(p)

            if roles:
                user.roles = roles

            user.save()
            self.stdout.write(self.style.SUCCESS(f"User {email!r} updated"))
        else:
            self.stdout.write(self.style.ERROR(f"User {email!r} not found"))

    def handle_list(self, *args: Any, **options: Any) -> Optional[str]:
        User = get_user_model()
        users = User.objects.all()
        self.stdout.write(self.style.WARNING(f"Total users: {len(users)}"))
        for r in users:
            roles = ", ".join([role.name for role in r.roles.all()])
            self.stdout.write(
                self.style.SUCCESS(f"* {r.email} - {r.fullname} [{roles}]")
            )

    def handle_drop(self, *args: Any, **options: Any) -> Optional[str]:
        User = get_user_model()
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Dropping user is complete"))

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        subcommand = options["sub"]
        if subcommand is None:
            self.print_help(sys.argv[0], "user")
            return

        handle = getattr(self, f"handle_{subcommand}")
        handle(*args, **options)
