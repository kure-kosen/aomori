from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt

from PIL import Image
import numpy as np

from analysis.views import get_target_contour_dict, get_shapes, Shapes

@csrf_exempt
def index(request):
    import datetime
    msg = datetime.datetime.now()
    context = {'msg': msg}
    if request.method == 'POST':
        img_origin = Image.open(request.FILES['image'])
        img = np.asarray(np.array(img_origin))
        shapes = get_shapes('', img_array=img)
        s = Shapes(shapes)
        result = s.action()
        print(result)
        context['file'] = result
        return render(request, 'frontend/index.html', context)
    else:
        return render(request, 'frontend/index.html', context)
