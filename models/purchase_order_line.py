from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Campo nuevo: columna real en BD, visible en Studio
    x_excedente_linea = fields.Float(
        string='Excedente por Línea',
        default=0.0,
        compute='_compute_excedente_linea',
        store=True,
        help='(Alcanzado + Subtotal) - Presupuesto'
    )

    # Solo dependemos de campos nativos y estables
    @api.depends('price_subtotal')
    def _compute_excedente_linea(self):
        """
        Fórmula solicitada:
            (x_studio_asignado + price_subtotal) - x_studio_en_el_presupuesto
        Usamos getattr para no romper si Studio mueve/cambia algo; si no están, usa 0.0.
        """
        for line in self:
            subtotal = line.price_subtotal or 0.0
            alcanzado = getattr(line, 'x_studio_asignado', 0.0) or 0.0
            presupuestado = getattr(line, 'x_studio_en_el_presupuesto', 0.0) or 0.0

            excedente = (alcanzado + subtotal) - presupuestado
            line.x_excedente_linea = excedente

            # Log para inspección en ~/logs/odoo.log
            _logger.info(
                "[EXC-LINEA] POL %s | subtotal=%.2f alcanzado=%.2f presupuestado=%.2f => excedente=%.2f",
                line.id, subtotal, alcanzado, presupuestado, excedente
            )
