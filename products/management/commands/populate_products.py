"""
Django management command to populate the database with categories, subcategories, and products.

Usage:
    python manage.py populate_products
"""

from django.core.management.base import BaseCommand
from products.models import Category, Subcategory, Product
from django.utils.text import slugify
import random


class Command(BaseCommand):
    help = 'Populate database with categories, subcategories, and sample products'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing data...')
        Product.objects.all().delete()
        Subcategory.objects.all().delete()
        Category.objects.all().delete()

        # Define categories with their subcategories
        categories_data = {
            'Office Supplies': {
                'icon': 'Clipboard',
                'show_in_navbar': True,
                'navbar_order': 1,
                'subcategories': [
                    'Writing Instruments',
                    'Desk Accessories',
                    'Filing & Organization',
                    'Correction & Adhesives'
                ]
            },
            'Paper Products': {
                'icon': 'FileText',
                'show_in_navbar': True,
                'navbar_order': 2,
                'subcategories': [
                    'Copy & Printer Paper',
                    'Notebooks & Pads',
                    'Envelopes & Mailers',
                    'Specialty Paper'
                ]
            },
            'Ink & Toner': {
                'icon': 'Droplet',
                'show_in_navbar': True,
                'navbar_order': 3,
                'subcategories': [
                    'Ink Cartridges',
                    'Toner Cartridges',
                    'Printer Ribbons',
                    'Refill Kits'
                ]
            },
            'Office Machines': {
                'icon': 'Printer',
                'show_in_navbar': True,
                'navbar_order': 4,
                'subcategories': [
                    'Printers & Scanners',
                    'Copiers & Fax Machines',
                    'Shredders',
                    'Laminators',
                    'Binding Machines'
                ]
            },
            'Technology': {
                'icon': 'Monitor',
                'show_in_navbar': True,
                'navbar_order': 5,
                'subcategories': [
                    'Computers & Laptops',
                    'Monitors & Displays',
                    'Keyboards & Mice',
                    'Networking Equipment',
                    'Cables & Adapters',
                    'Storage Devices'
                ]
            },
            'Furniture': {
                'icon': 'Armchair',
                'show_in_navbar': True,
                'navbar_order': 6,
                'subcategories': [
                    'Office Chairs',
                    'Desks & Tables',
                    'Filing Cabinets',
                    'Bookcases & Shelving',
                    'Conference Room Furniture'
                ]
            },
            'Storage': {
                'icon': 'Archive',
                'show_in_navbar': True,
                'navbar_order': 7,
                'subcategories': [
                    'Filing Cabinets',
                    'Storage Boxes',
                    'Shelving Units',
                    'Desk Organizers'
                ]
            }
        }

        # Sample products for each subcategory
        products_data = {
            # Office Supplies
            'Writing Instruments': [
                {'name': 'Ballpoint Pen Blue - Pack of 10', 'price': 15.99, 'brand': 'PaperMate'},
                {'name': 'Gel Pen Black - Pack of 5', 'price': 12.50, 'brand': 'Pilot'},
                {'name': 'Permanent Markers Assorted Colors', 'price': 22.00, 'brand': 'Sharpie'},
                {'name': 'Mechanical Pencil 0.5mm', 'price': 8.99, 'brand': 'Pentel'},
                {'name': 'Highlighter Set 6 Colors', 'price': 18.50, 'brand': 'Stabilo'},
            ],
            'Desk Accessories': [
                {'name': 'Heavy Duty Stapler with 1000 Staples', 'price': 24.99, 'brand': 'Swingline'},
                {'name': 'Executive Desk Organizer Set', 'price': 34.99, 'brand': 'Rolodex'},
                {'name': 'Tape Dispenser with Invisible Tape', 'price': 16.50, 'brand': 'Scotch'},
                {'name': 'Paper Clip Holder Magnetic', 'price': 9.99, 'brand': 'OfficeMate'},
                {'name': 'Letter Tray 3-Tier Black', 'price': 28.00, 'brand': 'Rubbermaid'},
            ],
            'Filing & Organization': [
                {'name': 'File Folders Letter Size - Pack of 100', 'price': 35.00, 'brand': 'Smead'},
                {'name': '3-Ring Binder 2 Inch Black', 'price': 12.99, 'brand': 'Avery'},
                {'name': 'Label Maker Portable', 'price': 89.99, 'brand': 'Dymo'},
                {'name': 'Sheet Protectors Clear - Pack of 50', 'price': 18.50, 'brand': 'Avery'},
                {'name': 'Hanging File Folders with Tabs', 'price': 42.00, 'brand': 'Pendaflex'},
            ],
            'Correction & Adhesives': [
                {'name': 'Correction Tape - Pack of 5', 'price': 14.99, 'brand': 'BIC'},
                {'name': 'White-Out Correction Fluid', 'price': 6.50, 'brand': 'Liquid Paper'},
                {'name': 'Glue Stick 40g - Pack of 6', 'price': 12.00, 'brand': 'Elmer\'s'},
                {'name': 'Super Glue Instant Adhesive', 'price': 8.99, 'brand': 'Gorilla'},
                {'name': 'Double-Sided Tape 1 Inch', 'price': 11.50, 'brand': 'Scotch'},
            ],

            # Paper Products
            'Copy & Printer Paper': [
                {'name': 'A4 Premium Copy Paper - 5 Reams', 'price': 75.00, 'brand': 'Xerox'},
                {'name': 'Letter Size Paper 92 Bright - 10 Reams', 'price': 145.00, 'brand': 'HP'},
                {'name': 'Colored Paper Assorted - 500 Sheets', 'price': 28.50, 'brand': 'Astrobrights'},
                {'name': 'Photo Paper Glossy A4 - 100 Sheets', 'price': 35.99, 'brand': 'Canon'},
            ],
            'Notebooks & Pads': [
                {'name': 'Spiral Notebook 200 Pages - Pack of 5', 'price': 22.99, 'brand': 'Mead'},
                {'name': 'Legal Pad Yellow - Pack of 12', 'price': 28.00, 'brand': 'Ampad'},
                {'name': 'Sticky Notes 3x3 Assorted - 24 Pads', 'price': 19.99, 'brand': 'Post-it'},
                {'name': 'Hardcover Journal A5', 'price': 16.50, 'brand': 'Moleskine'},
            ],
            'Envelopes & Mailers': [
                {'name': 'White Envelopes #10 - Box of 500', 'price': 32.00, 'brand': 'Quality Park'},
                {'name': 'Bubble Mailers 6x9 - Pack of 25', 'price': 24.99, 'brand': 'UPAKNSHIP'},
                {'name': 'Manila Envelopes 9x12 - 100 Count', 'price': 38.50, 'brand': 'Columbian'},
            ],
            'Specialty Paper': [
                {'name': 'Cardstock White 110lb - 250 Sheets', 'price': 42.00, 'brand': 'Neenah'},
                {'name': 'Resume Paper Ivory - 100 Sheets', 'price': 18.99, 'brand': 'Southworth'},
                {'name': 'Graph Paper Pad 8.5x11', 'price': 12.50, 'brand': 'Roaring Spring'},
            ],

            # Ink & Toner
            'Ink Cartridges': [
                {'name': 'HP 67XL Black Ink Cartridge', 'price': 89.00, 'brand': 'HP'},
                {'name': 'Canon PG-245XL Black Ink', 'price': 82.50, 'brand': 'Canon'},
                {'name': 'Epson 252XL Cyan Ink Cartridge', 'price': 45.99, 'brand': 'Epson'},
                {'name': 'Brother LC3033 Magenta Ink', 'price': 52.00, 'brand': 'Brother'},
            ],
            'Toner Cartridges': [
                {'name': 'HP 26A Black Toner Cartridge', 'price': 165.00, 'brand': 'HP'},
                {'name': 'Brother TN730 Standard Toner', 'price': 142.50, 'brand': 'Brother'},
                {'name': 'Canon 137 Black Toner', 'price': 158.99, 'brand': 'Canon'},
                {'name': 'Samsung MLT-D116L High Yield Toner', 'price': 175.00, 'brand': 'Samsung'},
            ],
            'Printer Ribbons': [
                {'name': 'Epson ERC-38 Black Ribbon', 'price': 18.50, 'brand': 'Epson'},
                {'name': 'Citizen DP600 Ribbon Cartridge', 'price': 22.00, 'brand': 'Citizen'},
            ],
            'Refill Kits': [
                {'name': 'HP Ink Refill Kit Black', 'price': 35.99, 'brand': 'InkJet Refill'},
                {'name': 'Canon Ink Refill Kit Color', 'price': 42.50, 'brand': 'InkJet Refill'},
            ],

            # Office Machines
            'Printers & Scanners': [
                {'name': 'HP LaserJet Pro M404n Printer', 'price': 899.00, 'brand': 'HP', 'product_type': 'new'},
                {'name': 'Canon PIXMA TR8620 All-in-One', 'price': 599.99, 'brand': 'Canon', 'product_type': 'new'},
                {'name': 'Epson WorkForce ES-500W Scanner', 'price': 749.00, 'brand': 'Epson', 'product_type': 'new'},
                {'name': 'Brother MFC-L2750DW Refurbished', 'price': 449.99, 'brand': 'Brother',
                 'product_type': 'refurbished', 'condition': 'Excellent'},
            ],
            'Copiers & Fax Machines': [
                {'name': 'Canon imageCLASS MF445dw Copier', 'price': 1299.00, 'brand': 'Canon', 'product_type': 'new'},
                {'name': 'Brother Fax-2940 Laser Fax', 'price': 349.99, 'brand': 'Brother', 'product_type': 'new'},
            ],
            'Shredders': [
                {'name': 'Fellowes Powershred 99Ci', 'price': 425.00, 'brand': 'Fellowes'},
                {'name': 'AmazonBasics 8-Sheet Cross-Cut', 'price': 89.99, 'brand': 'AmazonBasics'},
                {'name': 'Bonsaii 12-Sheet Heavy Duty', 'price': 165.00, 'brand': 'Bonsaii'},
            ],
            'Laminators': [
                {'name': 'Scotch TL906 Thermal Laminator', 'price': 125.00, 'brand': 'Scotch'},
                {'name': 'Apache AL13P Professional Laminator', 'price': 189.99, 'brand': 'Apache'},
            ],
            'Binding Machines': [
                {'name': 'Fellowes Quasar+ 500 Comb Binder', 'price': 275.00, 'brand': 'Fellowes'},
                {'name': 'Swingline GBC ProClick Binding', 'price': 185.50, 'brand': 'Swingline'},
            ],

            # Technology
            'Computers & Laptops': [
                {'name': 'Dell OptiPlex 7010 Desktop i7', 'price': 2499.00, 'brand': 'Dell', 'product_type': 'new'},
                {'name': 'HP EliteBook 840 G8 Laptop', 'price': 3199.00, 'brand': 'HP', 'product_type': 'new'},
                {'name': 'Lenovo ThinkCentre M720 Refurbished', 'price': 1299.99, 'brand': 'Lenovo',
                 'product_type': 'refurbished', 'condition': 'Very Good'},
                {'name': 'Apple MacBook Air M2 Rental', 'price': 4299.00, 'brand': 'Apple', 'product_type': 'rental',
                 'rental_price_daily': 75.00, 'rental_price_weekly': 450.00, 'rental_price_monthly': 1500.00},
            ],
            'Monitors & Displays': [
                {'name': 'Dell 27" 4K UHD Monitor', 'price': 899.00, 'brand': 'Dell'},
                {'name': 'LG 34" UltraWide Curved Monitor', 'price': 1199.00, 'brand': 'LG'},
                {'name': 'ASUS 24" Full HD Business Monitor', 'price': 349.99, 'brand': 'ASUS'},
            ],
            'Keyboards & Mice': [
                {'name': 'Logitech MX Keys Wireless Keyboard', 'price': 249.00, 'brand': 'Logitech'},
                {'name': 'Wireless Ergonomic Mouse', 'price': 29.99, 'brand': 'Microsoft'},
                {'name': 'Mechanical Gaming Keyboard RGB', 'price': 179.00, 'brand': 'Razer'},
            ],
            'Networking Equipment': [
                {'name': 'TP-Link WiFi 6 Router AX3000', 'price': 299.00, 'brand': 'TP-Link'},
                {'name': 'Netgear 8-Port Gigabit Switch', 'price': 125.00, 'brand': 'Netgear'},
                {'name': 'Ubiquiti UniFi Access Point', 'price': 385.00, 'brand': 'Ubiquiti'},
            ],
            'Cables & Adapters': [
                {'name': 'USB-C to HDMI Cable 6ft', 'price': 24.99, 'brand': 'Anker'},
                {'name': 'DisplayPort to DVI Adapter', 'price': 18.50, 'brand': 'Cable Matters'},
                {'name': 'Ethernet Cable Cat6 50ft', 'price': 22.00, 'brand': 'Mediabridge'},
            ],
            'Storage Devices': [
                {'name': 'Samsung 1TB SSD External Drive', 'price': 299.00, 'brand': 'Samsung'},
                {'name': 'WD 4TB External Hard Drive', 'price': 189.99, 'brand': 'Western Digital'},
                {'name': 'SanDisk 128GB USB Flash Drive', 'price': 32.50, 'brand': 'SanDisk'},
            ],

            # Furniture
            'Office Chairs': [
                {'name': 'Premium Ergonomic Office Chair', 'price': 299.00, 'brand': 'Herman Miller',
                 'product_type': 'new'},
                {'name': 'Mesh Back Executive Chair Black', 'price': 449.99, 'brand': 'Steelcase',
                 'product_type': 'new'},
                {'name': 'Task Chair with Lumbar Support', 'price': 185.00, 'brand': 'HON', 'product_type': 'new'},
                {'name': 'Conference Room Chair Set of 4', 'price': 599.00, 'brand': 'Office Star',
                 'product_type': 'new'},
            ],
            'Desks & Tables': [
                {'name': 'L-Shaped Executive Desk Mahogany', 'price': 1299.00, 'brand': 'Bush Business'},
                {'name': 'Standing Desk Adjustable Height', 'price': 899.00, 'brand': 'Uplift'},
                {'name': 'Conference Table 8ft Seats 10', 'price': 1899.00, 'brand': 'National Office'},
                {'name': 'Computer Desk with Hutch', 'price': 649.99, 'brand': 'Sauder'},
            ],
            'Filing Cabinets': [
                {'name': '4-Drawer Vertical File Cabinet', 'price': 425.00, 'brand': 'HON'},
                {'name': '2-Drawer Lateral File Cabinet Black', 'price': 289.99, 'brand': 'Lorell'},
                {'name': 'Mobile Pedestal File Cabinet', 'price': 199.00, 'brand': 'Bush Business'},
            ],
            'Bookcases & Shelving': [
                {'name': '5-Shelf Bookcase Cherry Finish', 'price': 249.00, 'brand': 'Sauder'},
                {'name': 'Wire Shelving Unit 48x24x72', 'price': 185.00, 'brand': 'Alera'},
                {'name': 'Cube Storage Organizer 9-Cube', 'price': 129.99, 'brand': 'ClosetMaid'},
            ],
            'Conference Room Furniture': [
                {'name': 'Conference Table with Power Outlets', 'price': 2499.00, 'brand': 'Mayline'},
                {'name': 'Executive Conference Chairs Set of 8', 'price': 1899.00, 'brand': 'Boss Office'},
                {'name': 'Presentation Board Mobile Whiteboard', 'price': 425.00, 'brand': 'Quartet'},
            ],

            # Storage - Filing Cabinets (different from Furniture)
            'Filing Cabinets': [
                {'name': 'Heavy Duty Filing Cabinet 4-Drawer', 'price': 525.00, 'brand': 'HON'},
                {'name': 'Steel File Cabinet with Lock', 'price': 399.99, 'brand': 'Safco'},
            ],
            'Storage Boxes': [
                {'name': 'Bankers Box Storage - Pack of 12', 'price': 42.00, 'brand': 'Bankers Box'},
                {'name': 'Plastic Storage Tote 18 Gallon', 'price': 18.99, 'brand': 'Sterilite'},
                {'name': 'Archive Storage Boxes Heavy Duty', 'price': 55.00, 'brand': 'Fellowes'},
            ],
            'Shelving Units': [
                {'name': 'Metal Storage Rack 5-Tier', 'price': 165.00, 'brand': 'Edsal'},
                {'name': 'Heavy Duty Shelving 48x24', 'price': 225.00, 'brand': 'Muscle Rack'},
            ],
            'Desk Organizers': [
                {'name': 'Mesh Desk Organizer 5-Compartment', 'price': 28.99, 'brand': 'Simple Houseware'},
                {'name': 'Wooden Desktop Organizer', 'price': 45.00, 'brand': 'MyGift'},
                {'name': 'Drawer Organizer Set', 'price': 22.50, 'brand': 'mDesign'},
            ],
        }

        # Sample descriptions
        sample_descriptions = [
            "High-quality office essential designed for professional use. Built to last with premium materials.",
            "Perfect for busy offices and home workspaces. Reliable performance you can count on.",
            "Professional-grade product that combines functionality with durability. Ideal for daily use.",
            "Essential office supply that meets all your business needs. Trusted by professionals worldwide.",
            "Premium quality product designed for efficiency and comfort in any workspace.",
        ]

        # Sample features
        sample_features = [
            "Durable construction",
            "Easy to use",
            "Professional quality",
            "Space-saving design",
            "Warranty included"
        ]

        # Create categories and subcategories
        for cat_name, cat_data in categories_data.items():
            self.stdout.write(f'Creating category: {cat_name}')

            category = Category.objects.create(
                name=cat_name,
                slug=slugify(cat_name),
                icon=cat_data['icon'],
                description=f"Browse our wide selection of {cat_name.lower()} for your office needs.",
                show_in_navbar=cat_data['show_in_navbar'],
                navbar_order=cat_data['navbar_order'],
                is_active=True
            )

            # Create subcategories
            for subcat_name in cat_data['subcategories']:
                self.stdout.write(f'  Creating subcategory: {subcat_name}')

                subcategory = Subcategory.objects.create(
                    name=subcat_name,
                    slug=slugify(subcat_name),
                    category=category,
                    description=f"Quality {subcat_name.lower()} for all your office requirements.",
                    is_active=True
                )

                # Create products for this subcategory
                if subcat_name in products_data:
                    for idx, prod_data in enumerate(products_data[subcat_name], 1):
                        sku = f"{slugify(cat_name)[:3].upper()}-{slugify(subcat_name)[:3].upper()}-{idx:04d}"

                        # Generate unique slug with counter to avoid duplicates
                        base_slug = slugify(prod_data['name'])
                        slug = base_slug
                        counter = 1
                        while Product.objects.filter(slug=slug).exists():
                            slug = f"{base_slug}-{counter}"
                            counter += 1

                        # Determine product type
                        product_type = prod_data.get('product_type', 'new')

                        # Create product
                        product = Product.objects.create(
                            name=prod_data['name'],
                            slug=slug,
                            sku=sku,
                            subcategory=subcategory,
                            brand=prod_data['brand'],
                            product_type=product_type,
                            price=prod_data['price'],
                            original_price=prod_data['price'] * 1.2 if random.choice([True, False]) else None,
                            discount=random.choice([0, 0, 0, 10, 15, 20]) if random.choice([True, False]) else 0,
                            stock_count=random.randint(5, 100),
                            in_stock=True,
                            description=random.choice(sample_descriptions),
                            features=random.sample(sample_features, 3),
                            specifications={
                                "Brand": prod_data['brand'],
                                "Type": product_type.title(),
                                "Warranty": "1 Year" if product_type == 'new' else "90 Days"
                            },
                            rating=round(random.uniform(4.0, 5.0), 1),
                            reviews=random.randint(5, 150),
                            is_active=True,
                            is_featured=random.choice([True, False, False, False]),  # 25% featured
                            condition=prod_data.get('condition', ''),
                            warranty_months=12 if product_type == 'new' else 3,
                            rental_price_daily=prod_data.get('rental_price_daily'),
                            rental_price_weekly=prod_data.get('rental_price_weekly'),
                            rental_price_monthly=prod_data.get('rental_price_monthly'),
                        )

                        self.stdout.write(f'    Created product: {prod_data["name"]} ({sku})')

        # Summary
        total_categories = Category.objects.count()
        total_subcategories = Subcategory.objects.count()
        total_products = Product.objects.count()

        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Categories created: {total_categories}'))
        self.stdout.write(self.style.SUCCESS(f'Subcategories created: {total_subcategories}'))
        self.stdout.write(self.style.SUCCESS(f'Products created: {total_products}'))
        self.stdout.write(self.style.SUCCESS('\nYou can now view your products in the admin panel!'))