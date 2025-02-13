import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

class CarRentalService(travel_pb2_grpc.CarRentalServicer):
    def BookCar(self, request, context):
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
