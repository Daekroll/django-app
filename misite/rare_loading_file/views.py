from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def upload_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("my_file"):
        my_file = request.FILES["my_file"]
        max_file_size = 1 * 1024 * 1024
        if my_file.size > max_file_size:
            print("Размер файла не должен превышать 1 МБ.")
            context = {'big_file': "Размер файла не должен превышать 1 МБ."}
            return render(request, "rare_loading_file/loading_file.html", context=context)
        fs = FileSystemStorage()
        file_name = fs.save(my_file.name, my_file)
    return render(request, "rare_loading_file/loading_file.html")



