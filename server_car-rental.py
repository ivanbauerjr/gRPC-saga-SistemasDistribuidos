import random
import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

import random
import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

class CarRentalService(travel_pb2_grpc.CarRentalServicer):
    def __init__(self):
        # Defina uma variável de controle para alternar entre aleatório e hardcoded
        self.use_hardcoded_response = False  # Altere para True para usar a resposta hardcoded

    def BookCar(self, request, context):
        if self.use_hardcoded_response:
            # Resposta hardcoded
            return travel_pb2.CarResponse(success=True, status="Carro alugado com sucesso!")  # Hardcoded
            #return travel_pb2.CarResponse(success=False, status="Carro não disponível.") # Hardcoded
        else:
            # Resposta aleatória
            if random.choice([True, False]):
                return travel_pb2.CarResponse(success=True, status="Carro alugado!")
            return travel_pb2.CarResponse(success=False, status="Carro não disponível.")

    def CancelCar(self, request, context):
        return travel_pb2.CancelResponse(success=True, message="Reserva de carro cancelada.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_CarRentalServicer_to_server(CarRentalService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Servidor de Aluguel de Carros rodando na porta 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
