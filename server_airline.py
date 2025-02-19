import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc
import random  # Para simular respostas variadas

class AirlineService(travel_pb2_grpc.AirlineServicer):
    def __init__(self):
        # Define uma variável para alternar entre aleatório e hardcoded
        self.use_hardcoded_response = True  # Altere para False para usar resposta aleatória
        
        # Dicionário para armazenar reservas de voos
        self.reservas = {}  # Formato: {request_id: status}

    #Tenta reservar um voo e armazena no dicionário para possível compensação.
    def BookFlight(self, request, context):
        request_id = f"{request.origin}-{request.destination}-{request.date}-{request.type}"
        
        if self.use_hardcoded_response:
            success = True
            status = "Passagem comprada com sucesso!"  
        else:
            success = random.choice([True, False])
            status = "Passagem comprada!" if success else "Voo indisponível."

        # Registra a reserva apenas se for bem-sucedida
        if success:
            self.reservas[request_id] = status

        return travel_pb2.FlightResponse(success=success, status=status)

    #Compensa (cancela) uma reserva de voo previamente feita.
    def CancelFlight(self, request, context):
        request_id = f"{request.origin}-{request.destination}-{request.date}"
        
        if request_id in self.reservas:
            del self.reservas[request_id]  # Remove a reserva
            return travel_pb2.CancelResponse(success=True, message="Passagem cancelada com sucesso.")
        else:
            return travel_pb2.CancelResponse(success=False, message="Nenhuma passagem encontrada para cancelamento.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_AirlineServicer_to_server(AirlineService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor de Passagens Aéreas rodando na porta 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
