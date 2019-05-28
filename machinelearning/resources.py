from tastypie.resources import ModelResource
from machinelearning.models import ParseSurveyData

class MachineLearningResource(ModelResource):
    class Meta:
        queryset = ParseSurveyData.objects.score_prediction()
        resource_name = 'score_prediction'
