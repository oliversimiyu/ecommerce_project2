from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payment.models import Transaction, PaymentReport
from orders.models import Order
from django.contrib.auth import get_user_model
from payment.reports import generate_daily_report, generate_weekly_report, generate_monthly_report
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Generates sample payment reports for testing'

    def __init__(self):
        super().__init__()
        self.User = get_user_model()
        # Create a sample user if it doesn't exist
        self.sample_user, created = self.User.objects.get_or_create(
            username='sample_customer',
            defaults={
                'email': 'sample@example.com',
                'first_name': 'Sample',
                'last_name': 'Customer',
                'is_active': True
            }
        )
        if created:
            self.sample_user.set_password('samplepass123')
            self.sample_user.save()

    def create_sample_order(self, date):
        order = Order.objects.create(
            user=self.sample_user,
            first_name=f"Sample{random.randint(1, 1000)}",
            last_name=f"Customer{random.randint(1, 1000)}",
            email=f"sample{random.randint(1, 1000)}@example.com",
            address=f"{random.randint(1, 999)} Sample Street",
            postal_code=f"{random.randint(10000, 99999)}",
            city="Sample City",
            created=timezone.make_aware(
                timezone.datetime.combine(
                    date,
                    timezone.datetime.min.time()
                ) + timedelta(
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
            ),
            paid=True
        )
        return order

    def handle(self, *args, **kwargs):
        # Generate sample transactions for the past 30 days
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)
        
        payment_methods = ['mpesa', 'card', 'bank']
        statuses = ['completed', 'failed', 'refunded']
        
        # Generate transactions with different dates
        current_date = start_date
        while current_date <= end_date:
            # Generate 5-15 transactions per day
            num_transactions = random.randint(5, 15)
            
            for _ in range(num_transactions):
                # Create a sample order first
                order = self.create_sample_order(current_date)
                
                amount = Decimal(random.uniform(100, 5000)).quantize(Decimal('0.01'))
                status = random.choices(
                    statuses, 
                    weights=[0.8, 0.1, 0.1]  # 80% completed, 10% failed, 10% refunded
                )[0]
                
                transaction = Transaction.objects.create(
                    transaction_id=f"SAMPLE-{current_date.strftime('%Y%m%d')}-{random.randint(1000, 9999)}",
                    order=order,
                    amount=amount,
                    payment_method=random.choice(payment_methods),
                    status=status,
                    reference_number=f"REF-{current_date.strftime('%Y%m%d')}-{random.randint(100, 999)}",
                    created_at=timezone.make_aware(
                        timezone.datetime.combine(
                            current_date,
                            timezone.datetime.min.time()
                        ) + timedelta(
                            hours=random.randint(0, 23),
                            minutes=random.randint(0, 59)
                        )
                    )
                )
                
                # Add sample payment details
                if transaction.payment_method == 'mpesa':
                    transaction.payment_details = {
                        'mpesa_receipt': f"MPESA{random.randint(10000000, 99999999)}",
                        'phone_number': f"+2547{random.randint(10000000, 99999999)}"
                    }
                elif transaction.payment_method == 'card':
                    transaction.payment_details = {
                        'card_type': random.choice(['visa', 'mastercard']),
                        'last4': f"{random.randint(1000, 9999)}"
                    }
                transaction.save()
            
            # Generate reports for this date
            self.stdout.write(f"Generating reports for {current_date}")
            generate_daily_report(current_date)
            generate_weekly_report(current_date)
            generate_monthly_report(current_date)
            
            current_date += timedelta(days=1)
        
        self.stdout.write(self.style.SUCCESS('Successfully generated sample reports'))
