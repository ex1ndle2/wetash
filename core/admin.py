from django.contrib import admin
import core.models as core_models
# Register your models here.
admin.site.register(core_models.User)
admin.site.register(core_models.Family)
admin.site.register(core_models.AirQuality)     
admin.site.register(core_models.Quest)  
admin.site.register(core_models.QuestCompletion)  
admin.site.register(core_models.Reward) 
admin.site.register(core_models.RewardRedemption)