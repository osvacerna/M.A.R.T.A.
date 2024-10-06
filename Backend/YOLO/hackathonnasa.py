import cv2
from ultralytics import YOLO
import random
import numpy as np
from PIL import Image
import urllib.request

def getMap(lat, lng):
    lat = str(lat)
    lng = str(lng)
    zoom = str(19)
    size = '640x640'

    url = 'https://maps.googleapis.com/maps/api/staticmap?center=' + lat + ','+ lng +'&zoom='+ zoom +'&size=' + size +'&maptype=satellite&key=MY_API_KEY'
    save_as = 'img.png'

    urllib.request.urlretrieve(url, save_as)

# 21.099583, -101.639620
def EnhanceBaldio(lat, lng):    
    #Obtiene una imagen dada unas coordenadas
    getMap(lat, lng)

    #Usa YOLO para reconocer terrenos baldios en imagenes satelitales
    img = cv2.imread("img.png")
    model = YOLO("YOLO/best.pt")
    results = model.predict(img)

    Img = Image.fromarray(np.array(results[0].plot()))

    #Iteramos sobre todos los baldios
    for box in results[0].boxes.xyxy:
        x,y,w,z = np.array(box).astype(int)
        Area = abs(w-x)*abs(z-y)
        k = int(Area/250)

        X = [random.randint(x, w) for _ in range(k)]
        Y = [random.randint(y, z) for _ in range(k)]

        flag = -1
        #Pintamos circulos verdes en los baldios simulando arbolitos
        for p in zip(X,Y):
            if flag == -1:
                img = cv2.circle(img, p, 8, (10, 120, 10), thickness = -1)
            else:
                img = cv2.circle(img, p, 8, (19, 95, 21), thickness = -1)
            flag *= -1
    img = Image.fromarray(img)

    #Unimos las imagenes para tener un resultado visual
    ancho1, alto1 = Img.size
    ancho2, alto2 = img.size

    nueva_imagen = Image.new('RGB', (ancho1 + ancho2, max(alto1, alto2)))

    # Pegar la primera imagen en la nueva imagen
    nueva_imagen.paste(Img, (0, 0))

    # Pegar la segunda imagen a la derecha de la primera
    nueva_imagen.paste(img, (ancho1, 0))

    nueva_imagen.save('static/imagen_concatenada.png')
    # nueva_imagen.show()
    return nueva_imagen
