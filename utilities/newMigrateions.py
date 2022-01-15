from django.conf import settings
import os

if __name__=="__main__":
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'hospital.settings'
    # settings.configure()
    for item in settings.INSTALLED_APPS:
        if 'apps' in item:
            if os.path.exists(item.split('.')) and os.path.exists(os.path.join(item.split('.'),'migrations')):
                for it in os.listdir(os.path.join(item.split('.'),'migrations')):
                    print(it)