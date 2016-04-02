""" Media system utility functions """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'

from django.core.exceptions import ValidationError
from django.conf import settings
from ninecms.utils.transliterate import transliterate
from subprocess import check_output, call, CalledProcessError
import os


def path_file_name(instance, context, filename):
    """ Get path file name
    Transliterate filename
    Filter out any empty component from list
    :param instance: the image field
    :param context: the context such as node field name
    :param filename: the file name
    :return: the path file name
    """
    page_type_name = transliterate(instance.node.page_type.name, True, True)
    context = transliterate(context, True, True)
    group = transliterate(instance.group, True, True)
    filename = transliterate(filename, True, True)
    return os.path.join(*filter(None, ('ninecms', page_type_name, context, group, filename)))


def image_path_file_name(instance, filename):
    """ Callback for image node field to get path file name
    :param instance: the image field
    :param filename: the file name
    :return: the path file name
    """
    return path_file_name(instance, 'image', filename)


def file_path_file_name(instance, filename):
    """ Callback for file node field to get path file name
    :param instance: the image field
    :param filename: the file name
    :return: the path file name
    """
    return path_file_name(instance, 'file', filename)


def video_path_file_name(instance, filename):
    """ Callback for video node field to get path file name
    :param instance: the image field
    :param filename: the file name
    :return: the path file name
    """
    return path_file_name(instance, 'video', filename)


def validate_ext(value, valid):
    """ Validate a file field value for allowed extensions
    :param value: the field file value to validate extension
    :param valid: the allowed extensions to validate against
    :return: None
    """
    ext = os.path.splitext(value.name)[1]  # [0] returns path filename
    if ext not in valid:
        raise ValidationError("Unsupported file extension.")


def validate_file_ext(value):
    """ Validate a file field value for allowed file extensions
    :param value: the value to validate
    :return: None
    """
    validate_ext(value, ['.txt', '.pdf', '.doc', '.docx', '.odt', '.xls', '.xlsx', '.ods'])


def validate_video_ext(value):
    """ Validate a video field value for allowed file extensions
    :param value: the value to validate
    :return: None
    """
    validate_ext(value, ['.mp4', '.mpeg', '.m4v', '.webm', '.ogg', '.ogv', '.flv', '.jpg'])


def find_all(filename):
    """ Get all path file names under the path of a given path file name
    Useful in order to get all files and files from image styles
    Used in media delete signal
    http://stackoverflow.com/questions/1724693/find-a-file-in-python
    :param filename: the absolute path file name to use
    :return: a list of all absolute path file names
    """
    path = os.path.dirname(filename)
    name = os.path.basename(filename)
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def delete_all(filename):
    """ Delete all files that `find_all` returns
    :param filename: the absolute path file name to use
    :return: None
    """
    for file in find_all(filename):
        os.remove(file)


def image_style(image, style):
    """ Return the url of different image style
    Construct appropriately if not exist
    See 9cms-crop.odt

    Available styles
     - thumbnail: create a thumbnail restricted to the smaller dimension
     - thumbnail-upscale: create a thumbnail that is upscaled if smaller
     - thumbnail-crop: create a thumbnail that is cropped to the exact dimension

    :param image: ImageFieldFile
    :param style: Specify style to return image
    :return: image url of specified style
    """
    if not image:  # pragma: nocover
        return image
    # original url full: /media/ninecms/basic/image/test.png
    url = image.url
    # original url without file: /media/ninecms/basic/image
    url_path = '/'.join(url.split('/')[:-1])
    # original path full: ~/ninecms/media/ninecms/basic/image/test.png
    img_path_file_name = str(image.file)
    # original file: test.png
    img_file_name = os.path.basename(img_path_file_name)

    # style url without file: /media/ninecms/basic/image/large
    style_url_path = '/'.join((url_path, style))
    # style url full: /media/ninecms/basic/image/large/test.png
    style_url = '/'.join((style_url_path, img_file_name))
    # style path without file: ~/ninecms/media/ninecms/basic/image/large
    style_path = os.path.join(os.path.dirname(img_path_file_name), style)
    # style path full: ~/ninecms/media/ninecms/basic/image/large/test.png
    style_path_file_name = os.path.join(style_path, img_file_name)

    # the style dict
    style_def = settings.IMAGE_STYLES[style]

    if not os.path.exists(style_path_file_name):
        if not os.path.exists(style_path):
            os.makedirs(style_path)
        by = chr(120)   # x
        plus = chr(43)  # +

        # remove original path file name as it may contain spaces, before splitting
        # exception: usually file not exists (db or memcached inconsistency)
        try:
            # noinspection PyUnresolvedReferences
            source_size_str = check_output(['identify', img_path_file_name]).decode()
        except CalledProcessError:  # pragma: nocover
            return url
        source_size_str = source_size_str[len(img_path_file_name):].split(' ')[2]

        source_size_array = source_size_str.split(by)
        source_size_x = int(source_size_array[0])
        source_size_y = int(source_size_array[1])
        target_size_x = style_def['size'][0]
        target_size_y = style_def['size'][1]
        target_size_str = str(target_size_x) + by + str(target_size_y)

        # thumbnail
        if style_def['type'] == 'thumbnail':
            if target_size_x > source_size_x and target_size_y > source_size_y:
                target_size_str = source_size_str
            call(['convert', img_path_file_name, '-thumbnail', target_size_str, '-antialias', style_path_file_name])

        # thumbnail-upscale
        elif style_def['type'] == 'thumbnail-upscale':
            call(['convert', img_path_file_name, '-thumbnail', target_size_str, '-antialias', style_path_file_name])

        # thumbnail-crop
        elif style_def['type'] == 'thumbnail-crop':
            source_ratio = float(source_size_x) / float(source_size_y)
            target_ratio = float(target_size_x) / float(target_size_y)
            if source_ratio > target_ratio:  # crop vertically
                crop_target_size_x = source_size_y * target_ratio
                crop_target_size_y = source_size_y
                offset = (source_size_x - crop_target_size_x) / 2
                crop_size_str = str(crop_target_size_x) + by + str(crop_target_size_y) + plus + str(offset) + plus + '0'
            else:  # crop horizontally
                crop_target_size_x = source_size_x
                crop_target_size_y = source_size_x / target_ratio
                offset = (source_size_y - crop_target_size_y) / 2
                crop_size_str = str(crop_target_size_x) + by + str(crop_target_size_y) + plus + '0' + plus + str(offset)
            call(['convert', img_path_file_name, '-crop', crop_size_str, style_path_file_name])
            call(['convert', style_path_file_name, '-thumbnail', target_size_str, '-antialias', style_path_file_name])
            # moderators ^ and \> for -thumbnail and -resize do not work consistently:
            # "invalid argument for option `-resize'"
            # call(['convert', path_file_name, '-thumbnail', target_size_str + '^', '-gravity', 'center', '-extent',
            #      target_size_str, '-antialias', style_path_file_name])

        # # crop
        # elif style_def['type'] == 'crop':
        #    call(['convert', img_path_file_name, '-gravity', 'center', '-crop', target_size_str, style_path_file_name])
        #     call(['convert', img_path_file_name, '-gravity', 'center', '-background', 'None', '-extent',
        #           target_size_str, style_path_file_name])
    return style_url
