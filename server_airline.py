import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc
import random  # Para simular respostas variadas

import random
import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

class AirlineService(travel_pb2_grpc.AirlineServicer):
    def __init__(self):
        # Defina uma variável de controle para alternar entre aleatório e hardcoded
        self.use_hardcoded_response = True  # Altere para True para usar a resposta hardcoded

    def BookFlight(self, request, context):
        if self.use_hardcoded_response:
            # Resposta hardcoded
            return travel_pb2.FlightResponse(success=True, status="Passagem comprada com sucesso!")  # Hardcoded
            #return travel_pb2.FlightResponse(success=False, status="Voo indisponível.") # Hardcoded
        else:
            # Resposta aleatória
            if random.choice([True, False]):
                return travel_pb2.FlightResponse(success=True, status="Passagem comprada!")
            return travel_pb2.FlightResponse(success=False, status="Voo indisponível.")

    def CancelFlight(self, request, context):
        return travel_pb2.CancelResponse(success=True, message="Passagem cancelada.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_AirlineServicer_to_server(AirlineService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor de Passagens Aéreas rodando na porta 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
