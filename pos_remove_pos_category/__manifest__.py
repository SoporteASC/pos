# -*- coding: utf-8 -*-
# Copyright (C) 2015-TODAY Akretion (<http://www.akretion.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'POS Remove POS Category',
    'version': '10.0.2.0.1',
    'author': 'Akretion, Camptocamp SA, ACSONE SA/NV, '
              'Odoo Community Association (OCA)',
    'category': 'Sales Management',
    'depends': [
        'point_of_sale',
    ],
    'demo': [],
    'website': 'https://github.com/OCA/pos',
    'data': [
        'views/assets.xml',
        'views/pos_view.xml',
        'views/pos_category_view.xml',
    ],
    'installable': True,
    'license': 'AGPL-3',
}
