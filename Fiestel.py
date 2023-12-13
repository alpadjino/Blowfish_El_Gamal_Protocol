from abc import ABC, abstractmethod

class Feistel(ABC):
    @abstractmethod
    def feistel(self, block_bytes, sboxes, iteraton_keys, IV, feistel_mode: bool):
        pass