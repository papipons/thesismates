from __future__ import absolute_import
from django.utils import timezone

from celery import shared_task
from datetime import datetime

from . import models as repo_m

@shared_task
def start_processing(uid, slug):
    project = repo_m.Project.objects.get(uid=uid, slug=slug)
    pdfs = repo_m.Document.objects.filter(owner=project)

    for pdf in pdfs:
        if pdf.official == True:
            pdf.convert_to_png()
            print "official"
        else:
            pdf.delete()
            print "unofficial"

    project_to_update = repo_m.Project.objects.filter(uid=uid, slug=slug)
    project_to_update.update(published_date=timezone.now())
    project_to_update.update(status="published")

