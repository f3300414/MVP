from FileSystem.models import Folder, File
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

class FileSerializer(ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'extension']

class FolderInheritanseSerializer(ModelSerializer):
    parent_folder_id = PrimaryKeyRelatedField(
        source='parent_folder', read_only=True)
    file = FileSerializer(source='containing_file', many=True)

    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent_folder_id','file']