import pathlib
from django.http import HttpResponse
from django.shortcuts import render

from visits.models import PageVisit


this_dir = pathlib.Path(__file__).resolve().parent
def home_view(request, *args, **Kwargs):
   return about_view(request, *args, **Kwargs)

def about_view(request, *args, **Kwargs):
    qs = PageVisit.objects.all()
    queryset = PageVisit.objects.filter(path=request.path)
    try:
        percent = (queryset.count() * 100) / qs.count()
    except:
        percent = 0

    my_title = "my page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": queryset.count(),
        "percent": percent,
        "total_count_visit": qs.count(),
    }

    html_template = "home.html"
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)

def my_old_home_pages_view(request, *args, **Kwargs):
    my_title = "my page"
    my_context = {
        "page_title": my_title
    }
  
    html_ = """
     <!DOCTYPE html>
<html>

<body>
    <h1> {page_title} anything?</h1>
</body>
</html>

""".format(**my_context)
    # html_file = this_dir / "home.html"
    # html_ = html_file.read_text()
    return HttpResponse(html_)