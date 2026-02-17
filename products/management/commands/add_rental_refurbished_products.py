# products/management/commands/add_rental_refurbished_products.py

from django.core.management.base import BaseCommand
from products.models import Category, Subcategory, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Add rental printers, LED displays and refurbished items'

    def handle(self, *args, **kwargs):
        self.stdout.write('Adding rental and refurbished products...')

        # Get or create categories
        office_machines, _ = Category.objects.get_or_create(
            name='Office Machines',
            defaults={
                'description': 'Printers, copiers, and office equipment',
                'show_in_navbar': True,
                'navbar_order': 4
            }
        )

        technology, _ = Category.objects.get_or_create(
            name='Technology',
            defaults={
                'description': 'Computers, displays, and tech equipment',
                'show_in_navbar': True,
                'navbar_order': 5
            }
        )

        furniture, _ = Category.objects.get_or_create(
            name='Furniture',
            defaults={
                'description': 'Office furniture and seating',
                'show_in_navbar': True,
                'navbar_order': 6
            }
        )

        # Get or create subcategories
        printers_sub, _ = Subcategory.objects.get_or_create(
            category=office_machines,
            name='Printers',
            defaults={'description': 'Commercial and office printers'}
        )

        displays_sub, _ = Subcategory.objects.get_or_create(
            category=technology,
            name='LED Displays',
            defaults={'description': 'LED screens and digital displays'}
        )

        office_desks_sub, _ = Subcategory.objects.get_or_create(
            category=furniture,
            name='Office Desks',
            defaults={'description': 'Desks and workstations'}
        )

        # ============================================
        # RENTAL PRODUCTS - Printers (3 items)
        # ============================================

        rental_printers = [
            {
                'name': 'HP LaserJet Enterprise M506dn Printer Rental',
                'sku': 'RENT-PRINT-001',
                'brand': 'HP',
                'subcategory': printers_sub,
                'description': 'High-speed monochrome laser printer for office use. Print speed up to 43 ppm. Network ready with duplex printing. Perfect for busy offices with high volume printing needs.',
                'price': Decimal('45.00'),
                'rental_price_daily': Decimal('45.00'),
                'rental_price_weekly': Decimal('270.00'),
                'rental_price_monthly': Decimal('900.00'),
                'min_rental_period': 1,
                'stock_count': 8,
                'is_featured': True,
                'discount': 0,
                'product_type': 'rental',
                'specifications': {
                    'Print Speed': '43 ppm',
                    'Print Technology': 'Laser',
                    'Color': 'Monochrome',
                    'Connectivity': 'Ethernet, USB',
                    'Duplex': 'Automatic',
                    'Paper Capacity': '550 sheets',
                    'Monthly Duty Cycle': '150,000 pages'
                },
                'features': [
                    'Fast 43 ppm printing',
                    'Network connectivity',
                    'Automatic duplex printing',
                    '550-sheet paper capacity',
                    'Energy efficient'
                ]
            },
            {
                'name': 'Canon imageCLASS MF445dw All-in-One Printer Rental',
                'sku': 'RENT-PRINT-002',
                'brand': 'Canon',
                'subcategory': printers_sub,
                'description': 'Multifunction laser printer with print, scan, copy, fax. Perfect for small to medium offices. Features 5-inch color touchscreen for easy operation.',
                'price': Decimal('55.00'),
                'rental_price_daily': Decimal('55.00'),
                'rental_price_weekly': Decimal('330.00'),
                'rental_price_monthly': Decimal('1100.00'),
                'min_rental_period': 1,
                'stock_count': 5,
                'is_featured': True,
                'discount': 0,
                'product_type': 'rental',
                'specifications': {
                    'Print Speed': '40 ppm',
                    'Functions': 'Print, Scan, Copy, Fax',
                    'Color': 'Monochrome',
                    'Connectivity': 'Wi-Fi, Ethernet, USB',
                    'Duplex': 'Automatic',
                    'ADF Capacity': '50 sheets',
                    'Touchscreen': '5-inch color'
                },
                'features': [
                    '4-in-1 functionality',
                    'Wireless connectivity',
                    '50-sheet auto document feeder',
                    'Color touchscreen',
                    'Mobile printing support'
                ]
            },
            {
                'name': 'Epson EcoTank L6270 Color Printer Rental',
                'sku': 'RENT-PRINT-003',
                'brand': 'Epson',
                'subcategory': printers_sub,
                'description': 'High-capacity ink tank color printer. Ultra-low running cost. All-in-one with print, scan, copy. Ideal for color document printing and photos.',
                'price': Decimal('40.00'),
                'rental_price_daily': Decimal('40.00'),
                'rental_price_weekly': Decimal('240.00'),
                'rental_price_monthly': Decimal('800.00'),
                'min_rental_period': 1,
                'stock_count': 10,
                'is_featured': False,
                'discount': 0,
                'product_type': 'rental',
                'specifications': {
                    'Print Speed': '15 ppm (color)',
                    'Tank System': 'EcoTank refillable',
                    'Color': 'Color',
                    'Connectivity': 'Wi-Fi, Wi-Fi Direct, Ethernet',
                    'Functions': 'Print, Scan, Copy',
                    'ADF': '30-sheet',
                    'Page Yield': 'Up to 7,500 color pages'
                },
                'features': [
                    'High-capacity ink tanks',
                    'Color printing capability',
                    'Low cost per page',
                    'Wireless connectivity',
                    'Compact design'
                ]
            },
        ]

        # ============================================
        # RENTAL PRODUCTS - LED Displays (3 items)
        # ============================================

        rental_led_displays = [
            {
                'name': 'P3.91 Indoor LED Display Screen Rental - 500x500mm',
                'sku': 'RENT-LED-001',
                'brand': 'Unilumin',
                'subcategory': displays_sub,
                'description': 'High-resolution P3.91mm indoor LED display panel. Perfect for events, exhibitions, conferences. Modular design allows creating custom screen sizes. Easy setup and teardown.',
                'price': Decimal('150.00'),
                'rental_price_daily': Decimal('150.00'),
                'rental_price_weekly': Decimal('850.00'),
                'rental_price_monthly': Decimal('3000.00'),
                'min_rental_period': 1,
                'stock_count': 50,
                'is_featured': True,
                'discount': 0,
                'product_type': 'rental',
                'specifications': {
                    'Pixel Pitch': '3.91mm',
                    'Panel Size': '500x500mm',
                    'Resolution': '128x128 pixels',
                    'Brightness': '1000 nits',
                    'Refresh Rate': '3840Hz',
                    'Viewing Angle': '140° horizontal',
                    'Weight': '7.5 kg/panel',
                    'Application': 'Indoor events',
                    'Setup': 'Quick lock system'
                },
                'features': [
                    'High resolution display',
                    'Modular design',
                    'Quick setup system',
                    'Seamless tiling',
                    'Professional grade'
                ]
            },
            {
                'name': 'P4.81 Outdoor LED Display Screen Rental - 500x1000mm',
                'sku': 'RENT-LED-002',
                'brand': 'Leyard',
                'subcategory': displays_sub,
                'description': 'Weatherproof outdoor LED display. Ideal for outdoor events, concerts, sports. High brightness for excellent visibility in direct sunlight. IP65 rated protection.',
                'price': Decimal('200.00'),
                'rental_price_daily': Decimal('200.00'),
                'rental_price_weekly': Decimal('1150.00'),
                'rental_price_monthly': Decimal('4000.00'),
                'min_rental_period': 1,
                'stock_count': 40,
                'is_featured': True,
                'discount': 0,
                'product_type': 'rental',
                'specifications': {
                    'Pixel Pitch': '4.81mm',
                    'Panel Size': '500x1000mm',
                    'Resolution': '104x208 pixels',
                    'Brightness': '5500 nits',
                    'Refresh Rate': '3840Hz',
                    'IP Rating': 'IP65 waterproof',
                    'Weight': '18 kg/panel',
                    'Application': 'Outdoor events',
                    'Viewing Distance': '5-50 meters'
                },
                'features': [
                    'Weatherproof IP65',
                    'Ultra-high brightness',
                    'Outdoor rated',
                    'Durable construction',
                    'Wide viewing angle'
                ]
            },
            {
                'name': '55" Samsung LED Video Wall Display Rental',
                'sku': 'RENT-LED-003',
                'brand': 'Samsung',
                'subcategory': displays_sub,
                'description': '55-inch ultra-narrow bezel video wall display. 1.7mm bezel for seamless multi-screen installations. 24/7 operation rated. Professional commercial display.',
                'price': Decimal('120.00'),
                'rental_price_daily': Decimal('120.00'),
                'rental_price_weekly': Decimal('700.00'),
                'rental_price_monthly': Decimal('2400.00'),
                'min_rental_period': 1,
                'stock_count': 20,
                'is_featured': False,
                'discount': 0,
                'product_type': 'rental',
                'specifications': {
                    'Screen Size': '55 inches',
                    'Bezel Width': '1.7mm',
                    'Resolution': '1920x1080 (Full HD)',
                    'Brightness': '500 nits',
                    'Contrast Ratio': '1400:1',
                    'Orientation': 'Portrait/Landscape',
                    'Connectivity': 'HDMI, DisplayPort, DVI',
                    'Operation': '24/7 rated'
                },
                'features': [
                    'Ultra-narrow bezel',
                    '24/7 operation',
                    'Full HD resolution',
                    'Multiple connectivity',
                    'Portrait/Landscape modes'
                ]
            },
        ]

        # ============================================
        # REFURBISHED PRODUCTS (2 items)
        # ============================================

        refurbished_products = [
            {
                'name': 'HP LaserJet Pro M404dn Printer - Refurbished',
                'sku': 'REFURB-PRINT-001',
                'brand': 'HP',
                'subcategory': printers_sub,
                'description': 'Professionally refurbished HP LaserJet. Tested and certified to work like new. Includes 90-day warranty. Print speed 38 ppm. Great value for budget-conscious buyers.',
                'price': Decimal('450.00'),
                'original_price': Decimal('750.00'),
                'stock_count': 4,
                'is_featured': True,
                'discount': 40,
                'product_type': 'refurbished',
                'condition': 'Excellent',
                'warranty_months': 3,
                'specifications': {
                    'Print Speed': '38 ppm',
                    'Print Technology': 'Laser',
                    'Connectivity': 'Ethernet, USB',
                    'Duplex': 'Automatic',
                    'Paper Capacity': '350 sheets',
                    'Condition': 'Excellent - Minimal wear',
                    'Warranty': '90 days',
                    'Includes': 'Power cable, starter toner'
                },
                'features': [
                    'Professionally refurbished',
                    '90-day warranty',
                    'Like-new performance',
                    'Network ready',
                    'Auto duplex printing'
                ]
            },
            {
                'name': 'Executive Office Desk L-Shape - Refurbished',
                'sku': 'REFURB-DESK-001',
                'brand': 'IKEA',
                'subcategory': office_desks_sub,
                'description': 'Premium L-shaped executive desk. Solid wood construction with walnut finish. Professionally restored and refinished. Minor cosmetic imperfections. Excellent structural integrity.',
                'price': Decimal('850.00'),
                'original_price': Decimal('1500.00'),
                'stock_count': 2,
                'is_featured': True,
                'discount': 43,
                'product_type': 'refurbished',
                'condition': 'Good',
                'warranty_months': 1,
                'weight': Decimal('65.00'),
                'specifications': {
                    'Dimensions': '160cm x 120cm x 75cm (H)',
                    'Material': 'Solid wood with veneer',
                    'Color': 'Walnut brown',
                    'Storage': '3 drawers with locks',
                    'Weight Capacity': '100 kg',
                    'Condition': 'Good - Some visible wear',
                    'Cable Management': 'Built-in grommets',
                    'Assembly': 'Required (tools included)'
                },
                'features': [
                    'L-shaped design',
                    'Solid wood construction',
                    'Locking drawers',
                    'Cable management',
                    'Spacious work surface'
                ]
            },
        ]

        # Create all products
        created_count = 0
        updated_count = 0

        # Add rental printers
        for product_data in rental_printers:
            product, created = Product.objects.update_or_create(
                sku=product_data['sku'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created rental printer: {product.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated rental printer: {product.name}'))

        # Add rental LED displays
        for product_data in rental_led_displays:
            product, created = Product.objects.update_or_create(
                sku=product_data['sku'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created rental LED display: {product.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated rental LED display: {product.name}'))

        # Add refurbished products
        for product_data in refurbished_products:
            product, created = Product.objects.update_or_create(
                sku=product_data['sku'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created refurbished item: {product.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated refurbished item: {product.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n🎉 Process completed!'))
        self.stdout.write(self.style.SUCCESS(f'   - Created: {created_count} products'))
        if updated_count > 0:
            self.stdout.write(self.style.WARNING(f'   - Updated: {updated_count} products'))
        self.stdout.write(self.style.SUCCESS(f'   - 3 Rental Printers'))
        self.stdout.write(self.style.SUCCESS(f'   - 3 Rental LED Displays'))
        self.stdout.write(self.style.SUCCESS(f'   - 2 Refurbished Items'))