from odoo import models, fields, api

# =========================
# Customer
===# =========================
class Customer(models.Model):
    _name = 'sales.customer'
    _description = 'Customer'

    name = fields.Char(required=True)
    email = fields.Char(required=True)
    phone = fields.Char()


# =========================
# Product
# =========================
class Product(models.Model):
    _name = 'sales.product'
    _description = 'Product'

    name = fields.Char(required=True)
    price = fields.Float(required=True)
    quantity_in_stock = fields.Integer(default=0)


# =========================
# Order
# =========================
class Order(models.Model):
    _name = 'sales.order'
    _description = 'Order'

    order_date = fields.Date(default=fields.Date.today)
    customer_id = fields.Many2one('sales.customer', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], default='draft')

    order_line_ids = fields.One2many('sales.order.line', 'order_id')

    total_price = fields.Float(compute="_compute_total_price", store=True)

    @api.depends('order_line_ids.price', 'order_line_ids.quantity')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(
                line.price * line.quantity
                for line in order.order_line_ids
            )

    def action_confirm(self):
        for order in self:
            order.state = 'confirmed'
# =========================
# Order Line
# =========================
class OrderLine(models.Model):
    _name = 'sales.order.line'
    _description = 'Order Line'

    order_id = fields.Many2one('sales.order', required=True, ondelete='cascade')
    product_id = fields.Many2one('sales.product', required=True)

    quantity = fields.Integer(default=1)

    price = fields.Float(related='product_id.price', store=True, readonly=True)



