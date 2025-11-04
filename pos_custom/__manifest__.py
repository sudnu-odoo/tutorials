{
    "name": "POS Custom",
    "version": "1.0",
    "summary": "POS Custom",
    "description": "A module to custom POS",
    "author": "Sultan",
    "depends": ["base", "point_of_sale"],
    "installable": True,
    "application": True,
    "category": "Tutorials",
    "data": [
        "views/pos_config_view.xml"
    ],
    "assets": {
        "point_of_sale._assets_pos": [
             "pos_custom/static/src/point_of_sale_override/**/*",
        ],
    },
}