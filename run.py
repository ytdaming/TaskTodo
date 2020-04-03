from myapp import manager
from myapp.models import User,Todo,Category
from myapp.views import *
if __name__ =='__main__':
    manager.run()