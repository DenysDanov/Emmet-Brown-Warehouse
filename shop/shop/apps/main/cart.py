from datetime import date, datetime, timedelta
import os
from random import choice
import string
import json
from redis  import Redis
from django.forms import model_to_dict
from django.conf import settings

from .models import Product
from .service import send_mail
from api.redis_servers import *

class Cart:
    def __init__(self, **kwargs) -> None:
        self.__id = kwargs.get('id') or self.__generateid()
        self.__product_list = json.loads(r.get(self.__id).decode()) if r.get(self.__id) else {}


        if kwargs.get('user'):
            if kwargs.get('user').is_authenticated:
                if not user_cart_store.exists(kwargs.get('user').id):
                    user_cart_store.mset(
                        {kwargs.get('user').id: self.id}
                        )
    

    def __getitem__(self, key : int):
        assert not isinstance(key, int) 
        return self.__product_list[key]

    @property
    def id(self):
        return self.__id
    
    def getproducts(self):
        cart = [model_to_dict(p) for p in Product.objects.filter(id__in=self.__product_list.keys())]
        qnts = list(self.__product_list.values())
        [
            cart[x].update({'quantity' : qnts[x]}) \
                for x in range(len(qnts)) 
        ]
        return cart

    def save(self):
        r.mset({self.__id: json.dumps(self.__product_list)})
        return self

    def addproduct(self, id, quantity):
        if id not in self.__product_list.keys():
            self.__product_list.update({id: quantity})
        else:
            self.__product_list.update({id: str(int(self.__product_list[id]) + int(quantity))})
        return self

    def deleteproduct(self, id):
        self.__product_list.pop(id)
        self.save()
        return self


    def order(self):
        c = self.getproducts()
        r.expire(self.__id, timedelta(seconds=5))
        header = 'Нове замовлення '+ str(datetime.now())
        r_c = [x['name'] + \
                '; Кількість: ' + \
                x['quantity'] + \
                '; Ціна: ' + \
                str(x['price']) + \
                '; Сума: ' + \
                str(x['price']*int(x['quantity']))
                for x in c]
        content = '\n'.join(r_c)
        send_mail(
            settings.SMTP_USER[0].replace('"', ''),
            settings.SMTP_USER[1].replace('"', ''),
            settings.ADMIN_MAIL,
            header,
            content
            )
        self.__product_list.clear()
        self.save()
        return self
        

    def delete(self):
        [self.__product_list.pop(id) for id in list(self.__product_list.keys())]
        self.save()
        return self
    
    def __generateid(self, length=32):
        '''Генерує унікальний для множини sequence ідентифікатор'''
        while True:
            temp_id = ''.join([choice(string.ascii_lowercase) for x in range(length)])
            if not r.exists(temp_id):
                
                return temp_id

