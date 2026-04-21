from odoo import models, fields, api
from odoo.exceptions import ValidationError

# =========================
# Customer (Added Inheritance)
# =========================
class Customer(models.Model):
    _name = 'sales.customer'
    # نقطة الـ Inheritance: ورثنا خصائص الـ mail.thread عشان نقدر نستخدم الشات واللوج
    _inherit = ['mail.thread'] 
    _description = 'Customer'

    name = fields.Char(required=True)
    email = fields.Char(required=True)
    phone = fields.Char()

# =========================
# Product (Added Python Constraints)
# =========================
class Product(models.Model):
    _name = 'sales.product'
    _description = 'Product'

    name = fields.Char(required=True)
    price = fields.Float(required=True)
    quantity_in_stock = fields.Integer(default=0)

    # نقطة الـ Constraints: بنمنع السيستم يقبل سعر أقل من أو يساوي صفر
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("السعر لازم يكون أكبر من صفر!")

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
# Order Line (Added Quantity Constraint)
# =========================
class OrderLine(models.Model):
    _name = 'sales.order.line'
    _description = 'Order Line'

    order_id = fields.Many2one('sales.order', required=True, ondelete='cascade')
    product_id = fields.Many2one('sales.product', required=True)
    quantity = fields.Integer(default=1)
    price = fields.Float(related='product_id.price', store=True, readonly=True)

    # نقطة الـ Constraints: بنمنع إضافة كمية صفر أو سالب
    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity <= 0:
                raise ValidationError("الكمية المبيعة لازم تكون حبة واحدة على الأقل!")
