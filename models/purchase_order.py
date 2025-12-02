from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    x_studio_excedente_total = fields.Float(
        string='Excedente Total',
        compute='_compute_excedente_total',
        store=True,
    )

    @api.depends('order_line.x_excedente_linea')
    def _compute_excedente_total(self):
        """Suma todos los excedentes por línea."""
        for order in self:
            order.x_studio_excedente_total = sum(
                (line.x_excedente_linea or 0.0) for line in order.order_line
            )
