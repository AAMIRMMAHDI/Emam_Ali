from rest_framework import serializers
from .models import User, Category, Question, ExamResult

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'category')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            category=validated_data['category']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SubmitExamSerializer(serializers.Serializer):
    answers = serializers.DictField()  # {question_id: 'A' یا 'B' ...}