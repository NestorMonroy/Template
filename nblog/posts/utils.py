import math
import os
import random
import re
import string
import datetime
from django.conf import settings
from django.utils.text import slugify

from django.utils.html import strip_tags


def count_words(html_string):
    # html_string = """
    # <h1>This is a title</h1>
    # """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)  # joincfe.com/projects/
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)  # assuming 200wpm reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 100000000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "post/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def upload_icon_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 100000000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "comment_thumbnail/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )

def upload_image_account_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1, 100000000)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext)
    return "post/accounts/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    """
    This is for a Django project with an key field
    """
    size = random.randint(30, 45)
    key = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key


def unique_order_id_generator(instance):
    """
    This is for a Django project with an order_id field
    """
    order_new_id = random_string_generator()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return order_new_id


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
