from django import template
from django.template import Library

from .. utils import has_samples
from .. utils import get_samples
register = Library()


class IfProductHasSamples(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.contents.split()
        if len(bits) != 1:
            raise template.TemplateSyntaxError(
                "'%s' tag takes one argument" % bits[0])
        end_tag = 'endifproducthassamples'
        nodelist_true = parser.parse(('else', end_tag))
        token = parser.next_token()
        if token.contents == 'else':  # there is an 'else' clause in the tag
            nodelist_false = parser.parse((end_tag,))
            parser.delete_first_token()
        else:
            nodelist_false = ""

        return cls(bits[0], nodelist_true, nodelist_false)

    def __init__(self, codename, nodelist_true, nodelist_false):
        self.codename = codename
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        product = context.get("product")

        if has_samples(product):
            return self.nodelist_true.render(context)

        return self.nodelist_false


@register.tag
def ifproducthassamples(parser, token):
    return IfProductHasSamples.handle_token(parser, token)


class ProductSamplesNode(template.Node):
    def render(self, context):
        product = context["product"]
        context["product_samples"] = get_samples(product=product)
        return ''


@register.tag
def product_samples(parser, token):
    return ProductSamplesNode()
