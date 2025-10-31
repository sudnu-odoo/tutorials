from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    amount_total_text = fields.Char(
        string="Amount in Words",
        compute="_compute_amount_total_text"
    )

    def _compute_amount_total_text(self):
        for move in self:
            if move.currency_id and move.amount_total:
                move.amount_total_text = move.currency_id.amount_to_text(move.amount_total)
            else:
                move.amount_total_text = ''
