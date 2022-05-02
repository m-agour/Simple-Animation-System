import os, json
from mesh import *


class Model:
    def __init__(self, path):
        self.meshes = []
        self.path = path
        self.model = glm.mat4()
        data = self.__loadAndGetData()
        for i in range(len(data['meshes'])):
            meshData = data['meshes'][i]
            self.meshes.append(Mesh(meshData, data['materials'][meshData['materialindex']]['properties']))

    def __loadAndGetData(self):
        data = None
        with open(self.path) as file:
            data = json.load(file)
        return data

    def draw(self, program):
        program.use()
        for mesh in self.meshes:
            mesh.draw(program)

    def __del__(self):
        self.delete()

    def delete(self):
        self.meshes.clear()