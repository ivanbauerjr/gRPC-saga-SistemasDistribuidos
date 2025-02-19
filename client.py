import grpc
from concurrent import futures
import travel_pb2
import travel_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = travel_pb2_grpc.TravelAgencyStub(channel)
        response = stub.BookTrip(
            travel_pb2.TripRequest(
                type="round-trip",
                date="2025-06-10",
                origin="Curitiba",
                destination="Rio de Janeiro",
                people=2
            )
        )
        print(f"Resultado da Reserva: {response.flight_status}, {response.hotel_status}, {response.car_status}")
        print(f"Mensagem: {response.message}")

if __name__ == "__main__":
    run()