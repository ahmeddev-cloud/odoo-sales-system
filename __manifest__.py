{
    'name': 'Sales Management System',
    'version': '1.0',
    'summary': 'Module for managing customers, products, and orders',
    'description': """
        Project SAD: Odoo custom module for sales system.
        - Manage Customers
        - Manage Products
        - Manage Orders and Order Lines
    """,
    'author': 'Ahmed Mahmoud',
    'website': 'https://github.com/ahmeddev-cloud/odoo-sales-system.git',
    'category': 'Sales',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/demo_data.xml'
    ],

    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
