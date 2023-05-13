from datetime import datetime, timezone
import datetime as dt
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from app.models import Tag,Snippet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SnippetAddSerializer(serializers.ModelSerializer):

    text = serializers.CharField(write_only=True, required=True)
    title = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Snippet
        fields = ['text','title']

    def create(self, validated_data):
        request = self.context.get('request', None)
        get_text = validated_data.get('text',None)
        get_title = validated_data.get('title', None)

        if not get_text:
            raise ValidationError({"error": "Text is Required"})
        if not get_title:
            raise ValidationError({"error": "Title is Required"})
        
        get_user = request.user
        check_title = Tag.objects.filter(title_name = str(get_title)).first()
        if check_title:
            create_snippet = Snippet(text=get_text,title=check_title,
                                   created_by=get_user.id)
            create_snippet.save()
        else:
            create_tag = Tag(title_name=get_title)
            create_tag.save()
            create_snippet = Snippet(text=get_text,title=create_tag,
                                   created_by=get_user.id)
            create_snippet.save()
        
        return create_snippet
    
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title_name']
    

class SnippetListSerializer(serializers.ModelSerializer):
    # title_name= serializers.CharField(source='title', read_only=True)
    title = TagSerializer()

    class Meta:
        model = Snippet
        fields = ['text', 'created_at','title']

class SnippetUpdateSerializer(serializers.ModelSerializer):

    text = serializers.CharField(write_only=True, required=True)
    title = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Snippet
        fields = ['text','title']

    def update(self, instance, validated_data):
        title_data = validated_data.pop('title')
        title = Tag.objects.get(pk=title_data)
        instance.text = validated_data.get('text', instance.text)
        instance.title = title
        instance.save()
        return instance
    
class SnippetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        fields = ['text', 'created_at','title']
    






        
       