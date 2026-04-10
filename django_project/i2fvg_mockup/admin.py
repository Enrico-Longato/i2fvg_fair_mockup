from django.contrib import admin

from i2fvg_mockup.models import (
    CompanyRegistryHeadquarters,
    CompanyRegistryFiltered,
    Financial,
    Project,
    Organization,
    EuroSciVoc,
)
    
admin.site.register(CompanyRegistryHeadquarters)
admin.site.register(CompanyRegistryFiltered)
admin.site.register(Financial)
admin.site.register(Project)
admin.site.register(Organization)
admin.site.register(EuroSciVoc)