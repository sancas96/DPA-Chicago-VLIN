import marbles.core
from marbles.mixins import mixins

class test_ingesta(marbles.core.TestCase, mixins.FileMixins):
    
    #def __init__(self, *args, **kwargs):
     #   marbles.core.TestCase.__init__(self, *args, **kwargs)
   
    
    def test_tamanio(self, nombre_archivo, tamanio_archivo):
        self.nombre_archivo=nombre_archivo
        self.tamanio_archivo=tamanio_archivo
        self.assertFileSizeGreater(self.nombre_archivo, self.tamanio_archivo, msg='El tamaño del archivo ingestado es muy pequeño')