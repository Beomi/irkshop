from __future__ import absolute_import

# 아래 import는 장고가 시작될 때 항상 import되기 때문에
# shared_task가 장고에서 작동하는 것을 가능하게 해 줍니다.
#from .celery import app as celery_app # Celery를 import합니다.