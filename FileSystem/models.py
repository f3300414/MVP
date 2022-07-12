from collections import deque
from django.db import models

class Folder(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'FileSystem'

    def __str__(self):
        return self.name

    @staticmethod
    def extract_children_folders(parent, all_folder):
        def children_filter(folder):
            return folder.parent_folder_id == parent.pk
        return list(filter(children_filter, all_folder))

    @staticmethod
    def extract_all_folders(ancestor, all_folder):
        result = [ancestor]
        children_queue = \
            deque(Folder.extract_children_folders(ancestor, all_folder))
        while len(children_queue) > 0:
            parent = children_queue.popleft()
            children_queue.extend(
                Folder.extract_children_folders(parent, all_folder))
            result.append(parent)
        return result

class File(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    extension = models.CharField(default='jpg', max_length=5, blank=False, null=False)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, blank=True, null=True, related_name='containing_file')
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'FileSystem'

    def __str__(self):
        return self.name
