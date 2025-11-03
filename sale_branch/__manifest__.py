{
    "name": "Sales Branch",
    "version": "1.0",
    "summary": "Sales Branch Management Module",
    "description": "A module to manage sales branches.",
    "author": "Sultan",
    "depends": ["base", "account", "sale"],
    "installable": True,
    "application": True,
    "category": "Tutorials",
    "data": [
        'views/sale_order_views.xml',
        'views/sale_branch_views.xml',
        'views/sale_branch_menus.xml',
        'security/ir.model.access.csv'
    ],
}