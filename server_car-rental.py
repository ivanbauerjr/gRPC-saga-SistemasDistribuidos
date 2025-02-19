import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc
import random  # Para simular respostas variadas

class CarRentalService(travel_pb2_grpc.CarRentalServicer):
    def __init__(self):
        # Define uma variável para alternar entre aleatório e hardcoded
        self.use_hardcoded_response = False  # Altere para True para usar resposta fixa
        
        # Dicionário para armazenar reservas de carros
        self.reservas = {}  # Formato: {request_id: status}

    #Tenta alugar um carro e armazena a reserva para possível compensação.
    def BookCar(self, request, context):
        request_id = request.destination + request.date 
        
        if self.use_hardcoded_response:
            success = True
            status = "Carro alugado com sucesso!"  
        else:
            success = random.choice([True, False])
            status = "Carro alugado!" if success else "Carro não disponível."

        # Registra a reserva apenas se for bem-sucedida
        if success:
            self.reservas[request_id] = status

        return travel_pb2.CarResponse(success=success, status=status)

    #Compensa (cancela) uma reserva de carro previamente feita.
    def CancelCar(self, request, context):
        request_id = request.destination + request.date
        
        if request_id in self.reservas:
            del self.reservas[request_id]  # Remove a reserva
            return travel_pb2.CancelResponse(success=True, message="Reserva de carro cancelada com sucesso.")
        else:
            return travel_pb2.CancelResponse(success=False, message="Nenhuma reserva de carro encontrada para cancelamento.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_CarRentalServicer_to_server(CarRentalService(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    print("Servidor de Aluguel de Carros rodando na porta 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
