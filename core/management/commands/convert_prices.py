import os
from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Convert all product prices from USD to KSH'

    def add_arguments(self, parser):
        parser.add_argument('--exchange-rate', type=float, default=130.0,
                           help='Exchange rate from USD to KSH (default: 130)')

    def handle(self, *args, **options):
        exchange_rate = options['exchange_rate']
        
        # Try to find the Item model
        try:
            # First try to import from core app (common name)
            Item = apps.get_model('core', 'Item')
            self.stdout.write(self.style.SUCCESS('Found Item model in core app'))
        except LookupError:
            try:
                # If not found, try to find it in any app
                for app_config in apps.get_app_configs():
                    for model in app_config.get_models():
                        if model.__name__ == 'Item':
                            Item = model
                            self.stdout.write(self.style.SUCCESS(f'Found Item model in {app_config.name} app'))
                            break
                    if 'Item' in locals():
                        break
            except:
                self.stdout.write(self.style.ERROR('Could not find Item model. Please check your app name.'))
                return
        
        if 'Item' not in locals():
            self.stdout.write(self.style.ERROR('Could not find Item model in any app.'))
            return
        
        # Update regular prices
        items = Item.objects.all()
        updated_count = 0
        
        for item in items:
            original_price = item.price
            item.price = round(item.price * exchange_rate, 2)
            
            if item.discount_price is not None:
                original_discount = item.discount_price
                item.discount_price = round(item.discount_price * exchange_rate, 2)
                self.stdout.write(
                    f'Updating {item.title}: ${original_price} → KSH{item.price}, '
                    f'Discount: ${original_discount} → KSH{item.discount_price}'
                )
            else:
                self.stdout.write(
                    f'Updating {item.title}: ${original_price} → KSH{item.price}'
                )
            
            item.save()
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully converted {updated_count} items from USD to KSH')
        )
        self.stdout.write(
            self.style.WARNING('NOTE: You also need to update Stripe settings to use KSH instead of USD')
        )