import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

class TravelAgencyService(travel_pb2_grpc.TravelAgencyServicer):
    def __init__(self):
        # Criar conexões gRPC para cada serviço
        self.airline_channel = grpc.insecure_channel('localhost:50051')
        self.airline_stub = travel_pb2_grpc.AirlineStub(self.airline_channel)

        self.hotel_channel = grpc.insecure_channel('localhost:50052')
        self.hotel_stub = travel_pb2_grpc.HotelStub(self.hotel_channel)

        self.car_channel = grpc.insecure_channel('localhost:50053')
        self.car_stub = travel_pb2_grpc.CarRentalStub(self.car_channel)

    def BookTrip(self, request, context):
        try:
            # Etapa 1: Compra da Passagem Aérea
            flight_response = self.airline_stub.BookFlight(request)
            if not flight_response.success:
                return travel_pb2.TripResponse(
                    success=False,
                    flight_status="Falha",
                    hotel_status="Não reservado",
                    car_status="Não reservado",
                    message="Falha ao comprar passagem aérea."
                )

            # Etapa 2: Reserva do Hotel
            hotel_request = travel_pb2.HotelRequest(destination=request.destination, date=request.date, nights=2)
            hotel_response = self.hotel_stub.BookHotel(hotel_request)
            if not hotel_response.success:
                # Falhou -> Cancelar passagem aérea
                self.airline_stub.CancelFlight(request)
                return travel_pb2.TripResponse(
                    success=False,
                    flight_status="Cancelado (era: " + flight_response.status + ")",
                    hotel_status="Falha",
                    car_status="Não reservado",
                    message="Falha ao reservar hotel. Passagem cancelada."
                )

            # Etapa 3: Reserva do Carro
            car_request = travel_pb2.CarRequest(destination=request.destination, date=request.date, days=3)
            car_response = self.car_stub.BookCar(car_request)
            if not car_response.success:
                # Salvar status antes de cancelar
                flight_status_before_cancel = flight_response.status
                hotel_status_before_cancel = hotel_response.status

                # Cancelamento
                self.hotel_stub.CancelHotel(hotel_request)
                self.airline_stub.CancelFlight(request)

                return travel_pb2.TripResponse(
                    success=False,
                    flight_status=f"Cancelado (era: {flight_status_before_cancel})",
                    hotel_status=f"Cancelado (era: {hotel_status_before_cancel})",
                    car_status="Falha",
                    message="Falha ao reservar carro. Hotel e passagem cancelados."
                )

            # Todas as etapas bem-sucedidas
            return travel_pb2.TripResponse(
                success=True,
                flight_status=flight_response.status,
                hotel_status=hotel_response.status,
                car_status=car_response.status,
                message="Pacote de viagem reservado com sucesso!"
            )

        except grpc.RpcError as e:
            return travel_pb2.TripResponse(success=False, message=f"Erro inesperado: {e.details()}")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    travel_pb2_grpc.add_TravelAgencyServicer_to_server(TravelAgencyService(), server)
    server.add_insecure_port('[::]:50050')
    server.start()
    print("Agência de Viagens rodando na porta 50050")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()