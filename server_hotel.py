import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

class HotelService(travel_pb2_grpc.HotelServicer):
    def BookHotel(self, request, context):
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
