from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_file_size(file_instance):
    file_size = file_instance.size
    print(file_size)
    if file_size >= 3e+6:
        raise ValidationError(_("The maximum file size that can be uploaded is 3MB"))
    else:
        return file_instance
