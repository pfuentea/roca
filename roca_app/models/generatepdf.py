from django.db import models
from django.views.generic import View
from django.template.loader import render_to_string
from ..utils import html_to_pdf
from django.http import HttpResponse

class GeneratePdf(View):
    def get(self, data, *args, **kwargs):
    #data = models.invoices.objects.get(id= 1434)
    
        open('temp.html', "w").write(render_to_string('test_cotizacion.html',data ))

    # Converting the HTML template into a PDF file
        pdf = html_to_pdf('temp.html')
            
            # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
