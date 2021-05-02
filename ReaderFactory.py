# -*- coding: utf-8 -*-
import os
import vtk


class ReaderFactory:
    @staticmethod
    def get(file_path: str, element_file_path: str = None):
        """return the reader for given file"""
        from AFexport.AFexportReader import AFexportReader
        from S3D.S3DReader import S3DExportReader
        from IDF.IDFImporter import IDFImporter
        from PCF.PCFImporter import PCFImporter
        from NetworkxJson.NetworkxJsonImporter import NetworksJsonImporter

        reader = None

        if not element_file_path:
            _, ext = os.path.splitext(file_path)
            if ext.lower() == '.stl':
                reader = vtk.vtkSTLReader()
                reader.SetFileName(file_path)
            elif ext.lower() == '.vrml':
                reader = vtk.vtkVRMLImporter()
                reader.SetFileName(file_path)
                reader.Read()
                reader.Update()
            elif ext.lower() == '.s3d':
                reader = S3DExportReader()
                reader.SetFileName(file_path)
            elif ext.lower() == '.idf':
                reader = IDFImporter()
                reader.SetFileName(file_path)
                reader.Read()
            elif ext.lower() == '.pcf':
                reader = PCFImporter()
                reader.SetFileName(file_path)
                reader.Read()
            elif ext.lower() == '.json':
                reader = NetworksJsonImporter()
                reader.SetFileName(file_path)
                reader.Read()
        else:
            reader = AFexportReader()
            reader.SetFileName(file_path, element_file_path)

        return reader
