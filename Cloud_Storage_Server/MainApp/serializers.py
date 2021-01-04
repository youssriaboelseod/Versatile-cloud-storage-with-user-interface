from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import *
from Cloud import settings
from pathlib import Path

class FileSerializer(serializers.ModelSerializer):

    class Meta():
        model = File
        fields = ('file', 'upload_date', 'user', 'extension', 'image')

    def create(self, validated_data):
     
        extension = Path(str(validated_data['file'])).suffix

        if extension == ".cfg":
            image = "cfg.jpg"
        elif extension == ".conf":
            image = "conf.jpg"
        elif extension == ".css": 
            image = "css.jpg"
        elif extension == ".db":
            image = "db.jpg"
        elif extension == ".dll":
            image = "dll.jpg"
        elif extension == ".docx":
            image = "docx.jpg"
        elif extension == ".exe":
            image = "exe.jpg"
        elif extension == ".gif":
            image = "gif.jpg"
        elif extension == ".html":
            image = "html.jpg"
        elif extension == ".java":
            image = "java.jpg"
        elif extension == ".php":
            image = "php.jpg"
        elif extension == ".js":
            image = "js.jpg"
        elif extension == ".json":
            image = "json.jpg"
        elif extension == ".mp3":
            image = "mp3.jpg"
        elif extension == ".mp4":
            image = "mp4.jpg"
        elif extension == ".pdf":
            image = "pdf.jpg"
        elif extension == ".psd":
            image = "psd.jpg"
        elif extension == ".py":
            image = "py.jpg"
        elif extension == ".rar":
            image = "rar.jpg"
        elif extension == ".sql" or extension == ".sqlite3":
            image = "sql.jpg"
        elif extension == ".txt":
            image = "txt.jpg"
        elif extension == ".xml" or extension == ".ods":
            image = "xml.jpg"
        elif extension == ".zip":
            image = "zip.jpg"
        elif extension == ".img" or extension == ".png" or extension == ".jpg" or extension == ".ico":
            image = "img.jpg"
        else:
            image = "file.jpg"

        file_data = File(
            user = validated_data['user'],
            file = validated_data['file'],
            extension = extension,
            image = image,
        )

        file_data.save()
        return file_data


class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('username', 'email', 'password')
            extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            user.set_password(validated_data['password'])
            user.save()
            Token.objects.create(user=user)
            return user



