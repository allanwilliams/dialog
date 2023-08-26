from rest_framework.serializers import ModelSerializer

class GenericAllSerializer(ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'
        depth = 2
    
    
    
    def create(self, validated_data):
        print("@@@@@@@@@@@@@@@@@@@@",validated_data)
        return super().create(validated_data)