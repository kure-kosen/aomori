from django.shortcuts import render
from django.http import HttpResponse

import cv2
import numpy as np
import matplotlib.pyplot as plt

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def get_target_contour_dict():
    target_names = ['rectangle', 'triangle', 'circle']
    target_contour_dict = {}

    for target_name in target_names:
        target_path = f'datasets/targets/{target_name}.png'
        target = cv2.imread(target_path)
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

        target_preprocessed = cv2.GaussianBlur(target_gray, (5, 5), 0)
        _, target_binary = cv2.threshold(target_preprocessed, 130, 255, cv2.THRESH_BINARY)
        target_binary = cv2.bitwise_not(target_binary)

        _, contours, _ = cv2.findContours(target_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        target_contour_dict[target_name] = contours[0]

        cv2.drawContours(target, target_contour_dict[target_name], -1, (0,0,255), 3)

        target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
    return target_contour_dict

def get_shapes(img_path, img_array=None):
    # tar = 'datasets/test.png'
    if img_array is None:
        tegaki = cv2.imread(img_path)
    else:
        tegaki = img_array
    tegaki_gray = cv2.cvtColor(tegaki, cv2.COLOR_BGR2GRAY)

    tegaki_preprocessed = cv2.GaussianBlur(tegaki_gray, (5, 5), 0)
    _, tegaki_binary = cv2.threshold(tegaki_preprocessed, 145, 255, cv2.THRESH_BINARY_INV)

    _, tegaki_contours, _ = cv2.findContours(tegaki_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    height, width, _ = tegaki.shape

    min_im_area = (height / 50) * (width / 50)
    large_contours = [cnt for cnt in tegaki_contours if cv2.contourArea(cnt) > min_im_area]

    # BGRからRGBに変換して画像読込み
    # PILで読み込むとすでにRGBになっているようでいらないみたい
    # tegaki = cv2.cvtColor(tegaki, cv2.COLOR_BGR2RGB)

    target_contour_dict = get_target_contour_dict()

    shapes = []

    # 対象の図形の判定と中心の導出
    for large_contour in large_contours:
        shape = {}
        shape['contour'] = large_contour
        shape['similarity'] = 0.1
        shape['name'] = 'other'
        for target_name, target_contour in target_contour_dict.items():
            similarity = cv2.matchShapes(target_contour, shape['contour'],1,0.0)
            if shape['similarity'] > similarity:
                shape['similarity'] = similarity
                shape['name'] = target_name
        shape['moments'] = cv2.moments(shape['contour'])
        shape['x'] = int(shape['moments']['m10']/shape['moments']['m00'])
        shape['y'] = int(shape['moments']['m01']/shape['moments']['m00'])
        if shape['name'] != 'other':
            shapes.append(shape)
        else:
            pass

    # 色の判定と描画
    hsv = cv2.cvtColor(tegaki, cv2.COLOR_RGB2HSV)
    for shape in shapes:
        shape['hsv'] = hsv[shape['y'], shape['x']]
        if 50 < shape['hsv'][0] < 80 and shape['hsv'][1] >100  and shape['hsv'][2] > 100:
            shape['color'] = 'green'
        elif 90 < shape['hsv'][0] < 126 and shape['hsv'][1] >150  and shape['hsv'][2] > 130:
            shape['color'] = 'blue'
        elif (169 < shape['hsv'][0] < 179 or 0 < shape['hsv'][0] < 25) and shape['hsv'][1] >150 and shape['hsv'][2] > 190:
            shape['color'] = 'orange'
        elif 0 < shape['hsv'][0] < 179 and shape['hsv'][1] < 50 and shape['hsv'][2] < 100:
            shape['color'] = 'gray'
        else:
            shape['color'] = 'other'
        cv2.drawContours(tegaki, shape['contour'], -1, (255, 0, 0), 5)

    # x座標昇順にソート
    shapes = sorted(shapes, key=lambda x:x['x'])
    return (shapes, tegaki)


class Shapes:
    state = 'nomal'
    num = 0
    count = 0
    repeat_count = 0

    def __init__(self, shapes):
        self.shapes = shapes

    def get_shape(self):
        return self.shapes[self.num]

    def get_prev_shape(self):
        return self.shapes[self.num - 1] if i > 0 else self.shapes[-1]

    def get_next_shape(self):
        return self.shapes[self.num + 1] if self.num != len(self.shapes) - 1 else self.shapes[0]

    def get_next_triangle_num(self):
        for i in range(self.num + 1, len(self.shapes)):
            if self.shapes[i]['name'] == 'triangle':
                return i
        return None

    def action(self):
        self.result = ''
        while self.num < len(self.shapes):
            if self.shapes[self.num]['name'] == 'rectangle':
                pass
            elif self.shapes[self.num]['name'] == 'triangle':
                self._triangle()
            elif self.shapes[self.num]['name'] == 'circle':
                self._circle()
            self._next()
        return self.result

    def reset(self):
        self.state = 'nomal'
        self.num = 0
        self.result = ''

    def _rectangle(self):
        import datetime
        return datetime.datetime.now().minute % 2 == 0

    def _triangle(self):
        if self.get_next_shape()['name'] == 'rectangle':
            if self._rectangle():
                self.state = 'if'
            else:
                self.num = self.get_next_triangle_num()
                self.state = 'else'
        else:
            if self.state == 'nomal':
                self.repeat_start_num = self.num
                self.state = 'repeat'
            elif self.state == 'repeat':
                if self.repeat_count > 4:
                    self.state = 'nomal'
                else:
                    self.num = self.repeat_start_num
                    self.repeat_count += 1
            elif self.state == 'if':
                self.num = self.get_next_triangle_num()
                self.state = 'nomal'
            elif self.state == 'else':
                self.state = 'nomal'

    def _circle(self):
        print('circle', self.num)
        self.count += 1
        self.result += f'[{self.count}]: corcle {self.num}\n'
        return 0

    def _next(self):
        self.num += 1
