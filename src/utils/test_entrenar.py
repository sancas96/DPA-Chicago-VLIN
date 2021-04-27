import marbles.core
from marbles.mixins import mixins

class test_entrena(marbles.core.TestCase, mixins.FileMixins):
    
    def test_tamanio(self, nombre_archivo, tamanio_archivo):
        self.nombre_archivo=nombre_archivo
        self.tamanio_archivo=tamanio_archivo
        self.assertFileSizeGreater(self.nombre_archivo, self.tamanio_archivo, msg='El tamaño del archivo almacenado en S3 es muy pequeño')