from django.core.management.base import BaseCommand
from bus.models import Bus


class Command(BaseCommand):
    help = "Create SmartBus bus records"

    def handle(self, *args, **options):

        buses = [
            {
                "bus_number": "46",
                "time": "07:50:00",
                "destination": "Shanmuga Industries Arts and Science College",
            },
            {
                "bus_number": "5",
                "time": "07:50:00",
                "destination": "Shanmuga Industries Arts and Science College",
            },
        ]

        for data in buses:
            bus, created = Bus.objects.get_or_create(
                bus_number=data["bus_number"],
                defaults={
                    "time": data["time"],
                    "destination": data["destination"],
                    "latitude": 12.5036,
                    "longitude": 79.0608,
                }
            )

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Bus {bus.bus_number} created successfully"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Bus {bus.bus_number} already exists"
                    )
                )