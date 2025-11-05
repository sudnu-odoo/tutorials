{
    "name": "Custom Sale Access",
    "version": "1.0",
    "summary": "Custom Sale Accesss Module",
    "description": "A module to custom sale access module",
    "author": "Sultan",
    "depends": ["base", "sales_team", "sale_management"],
    "installable": True,
    "category": "Tutorials",
    "data": [
        "security/sale_custom_rules.xml",
        "security/ir.model.access.csv"
    ],
}