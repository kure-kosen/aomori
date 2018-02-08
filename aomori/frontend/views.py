from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from PIL import Image
import numpy as np
from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile


from analysis.views import get_target_contour_dict, get_shapes, Shapes
from images.models import ImageFile
from io import BytesIO

@csrf_exempt
def index(request):
    imagefile_list = ImageFile.objects.order_by('-created')
    return render(request, 'frontend/index.html', {'images': imagefile_list})
    if request.method == 'POST':
        img_original = Image.open(request.FILES['image'])
        img = np.asarray(np.array(img_original))
        shapes, _ = get_shapes('', img_array=img)
        s = Shapes(shapes)
        result = s.action()
        print(result)
        context['file'] = result
        return render(request, 'frontend/index.html', context)
    else:
        return render(request, 'frontend/index.html', context)


def upload_form(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bio_original = BytesIO()
            bio_result = BytesIO()
            pil_original = Image.open(request.FILES['original'])

            cv2_original = np.asarray(np.array(pil_original))
            shapes, cv2_result = get_shapes('', img_array=cv2_original)
            pil_result = Image.fromarray(cv2_result)

            pil_original.save(bio_original, format='PNG')
            pil_result.save(bio_result, format='PNG')
            img_original = InMemoryUploadedFile(bio_original, None, 'original.png', 'image/png', bio_original.getbuffer().nbytes, None)
            img_result = InMemoryUploadedFile(bio_result, None, 'result.png', 'image/png', bio_result.getbuffer().nbytes, None)

            m = ImageFile(original=img_original, result=img_result, )
            m.save()
            return redirect('frontend:result', imagefile_id=m.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'frontend/upload.html', {'form': form})

def result(request, imagefile_id):
    imagefile_instance = get_object_or_404(ImageFile, pk=imagefile_id)
    pil_original = Image.open(imagefile_instance.original)
    cv2_original = np.asarray(np.array(pil_original))
    shapes, cv2_result = get_shapes('', img_array=cv2_original)
    s = Shapes(shapes)
    result = s.action()
    return render(request, 'frontend/result.html', {'image': imagefile_instance, 'result': result})

class ImageUploadForm(forms.Form):
    original = forms.ImageField()

