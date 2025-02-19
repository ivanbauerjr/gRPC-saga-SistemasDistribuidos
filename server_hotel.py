import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc
import random

class HotelService(travel_pb2_grpc.HotelServicer):
    def __init__(self):
        # Defina uma variável para alternar entre aleatório e hardcoded
        self.use_hardcoded_response = True  # Altere para True para resposta fixa

        # Dicionário para armazenar reservas de hotéis
        self.reservas = {}  # Formato: {request_id: status}

    #Tenta reservar um hotel e armazena a reserva para possível compensação.
    def BookHotel(self, request, context):
        request_id = request.destination + request.date

        if self.use_hardcoded_response:
            success = True
            status = "Hotel reservado com sucesso!"
        else:
            success = random.choice([True, False])
            status = "Hotel reservado!" if success else "Hotel sem disponibilidade."

        # Registra a reserva apenas se for bem-sucedida
        if success:
            self.reservas[request_id] = status

        return travel_pb2.HotelResponse(success=success, status=status)

    #Compensa (cancela) uma reserva de hotel previamente feita.
    def CancelHotel(self, request, context):
        request_id = request.destination + request.date

        if request_id in self.reservas:
            del self.reservas[request_id]  # Remove a reserva
            return travel_pb2.CancelResponse(success=True, message="Reserva de hotel cancelada com sucesso.")
        else:
            return travel_pb2.CancelResponse(success=False, message="Nenhuma reserva de hotel encontrada para cancelamento.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_HotelServicer_to_server(HotelService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Servidor de Hotel rodando na porta 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
