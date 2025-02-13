import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc
import random

import random
import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

class HotelService(travel_pb2_grpc.HotelServicer):
    def __init__(self):
        # Defina uma variável de controle para alternar entre aleatório e hardcoded
        self.use_hardcoded_response = True  # Altere para True para usar a resposta hardcoded
        
    def BookHotel(self, request, context):
        if self.use_hardcoded_response:
            # Resposta hardcoded
            return travel_pb2.HotelResponse(success=True, status="Hotel reservado com sucesso!")  # Hardcoded
            #return travel_pb2.HotelResponse(success=False, status="Hotel sem disponibilidade.")  # Hardcoded
        else:
            # Resposta aleatória
            if random.choice([True, False]):
                return travel_pb2.HotelResponse(success=True, status="Hotel reservado!")
            return travel_pb2.HotelResponse(success=False, status="Hotel sem disponibilidade.")

    def CancelHotel(self, request, context):
        return travel_pb2.CancelResponse(success=True, message="Reserva de hotel cancelada.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_HotelServicer_to_server(HotelService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Servidor de Hotel rodando na porta 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
