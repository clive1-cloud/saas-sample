import pathlib
from django.http import HttpResponse
from django.shortcuts import render

from visits.models import PageVisit


this_dir = pathlib.Path(__file__).resolve().parent
def home_pages_view(request, *args, **Kwargs):
    qs = PageVisit.objects.all()
    queryset = PageVisit.objects.filter(path=request.path)

    my_title = "my page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": queryset.count(),
        "percent":(queryset.count() *100.0) /qs.count(),
        "total_count_visit": qs.count(),
    }

    path = request.path
    print("path", path)
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