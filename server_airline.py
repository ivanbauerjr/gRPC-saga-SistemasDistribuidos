import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc
import random  # Para simular respostas variadas

class AirlineService(travel_pb2_grpc.AirlineServicer):
    def BookFlight(self, request, context):
        if random.choice([True, False]):  # Simula sucesso ou falha
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
