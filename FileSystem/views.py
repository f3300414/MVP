from django.db.models import F, Q
from FileSystem.models import Folder, File
from FileSystem.serializer import FolderInheritanseSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class FolderViewSet(APIView):
    def get(self, request):
        root_folder = Folder.objects.filter(pk=11112)
        if not root_folder.exists():
            return Response({})
        all_folders = Folder.objects.all()
        result = Folder.extract_all_folders(root_folder[0], all_folders)
        serializer = FolderInheritanseSerializer(result, many=True)
        return Response(serializer.data)

    def post(self, request):
        folder_name = request.data['name']
        if Folder.objects.filter(name=folder_name).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        folder_info = request.data
        Folder.objects.create(**folder_info)
        return Response()

    def delete(self, request):
        delete_id = request.data['id']
        Folder.objects.get(pk=delete_id).delete()
        return Response()

    def put(self, request):
        #Create test folders
        root_folder = Folder.objects.create(name='layer_1_parent_0_id_1')
        parent_folder_dict = [root_folder.pk]
        for layer in range(2,6):
            datas = []
            for parent in parent_folder_dict:
                for folder in range(1,11):
                    folder_name = 'layer_'+str(layer) +'_parent_'+str(parent)+'_id_' + str(folder)
                    datas.append({'name': folder_name, 'parent_folder_id': parent})
            django_list = [Folder(**vals) for vals in datas]
            Folder.objects.bulk_create(django_list)
            parent_folder_dict = []
            for folder_info in datas:
                folder_pk = Folder.objects.get(name=folder_info['name']).pk
                parent_folder_dict.append(folder_pk)
        return Response()

class FileViewSet(APIView):
    def post(self, request):
        file_name = request.data['name']
        if File.objects.filter(name=file_name).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        file_info = request.data
        File.objects.create(**file_info)
        return Response()

    def get(self, request):
        identifier = request.data['identifier']
        result = Folder.objects.filter(Q(name__icontains=identifier) | Q(containing_file__name__icontains=identifier))\
                       .distinct()
        serializer = FolderInheritanseSerializer(result, many=True)
        return Response(serializer.data)

    def put(self, request):
        #Create test files
        all_folders = Folder.objects.all()
        for folder in all_folders:
            datas = []
            for fileId in range(1,11):
                file_name = folder.name+'_fid_'+str(fileId)+'.jpg'
                datas.append({'name': file_name, 'extension': 'jpg', 'folder_id': folder.pk})
            django_list = [File(**vals) for vals in datas]
            File.objects.bulk_create(django_list)
        return Response()

    def delete(self, request):
        delete_id = request.data['id']
        File.objects.get(pk=delete_id).delete()
        return Response()