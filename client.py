import grpc
import travel_pb2
import travel_pb2_grpc
import tkinter as tk
from tkinter import messagebox

# Função para reservar a viagem
def book_trip():
    with grpc.insecure_channel('localhost:50050') as channel:
        stub = travel_pb2_grpc.TravelAgencyStub(channel)

        response = stub.BookTrip(
            travel_pb2.TripRequest(
                type=trip_type_var.get(),
                date=date_entry.get(),
                origin=origin_entry.get(),
                destination=destination_entry.get(),
                people=int(people_entry.get())
            )
        )

        messagebox.showinfo(
            "Resultado da Reserva",
            f"Voo: {response.flight_status}\n"
            f"Hotel: {response.hotel_status}\n"
            f"Carro: {response.car_status}\n\n"
            f"Mensagem: {response.message}"
        )

# Criando a UI
root = tk.Tk()
root.title("Reserva de Viagem")

tk.Label(root, text="Tipo de Viagem:").grid(row=0, column=0)
trip_type_var = tk.StringVar(value="ida-e-volta")
tk.Entry(root, textvariable=trip_type_var).grid(row=0, column=1)

tk.Label(root, text="Data de ida:").grid(row=1, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=1, column=1)

tk.Label(root, text="Data de volta:").grid(row=2, column=0)
return_date_entry = tk.Entry(root)
return_date_entry.grid(row=2, column=1)

tk.Label(root, text="Origem:").grid(row=3, column=0)
origin_entry = tk.Entry(root)
origin_entry.grid(row=3, column=1)

tk.Label(root, text="Destino:").grid(row=4, column=0)
destination_entry = tk.Entry(root)
destination_entry.grid(row=4, column=1)

tk.Label(root, text="Pessoas:").grid(row=5, column=0)
people_entry = tk.Entry(root)
people_entry.grid(row=5, column=1)

tk.Button(root, text="Reservar", command=book_trip).grid(row=6, column=0, columnspan=2)

root.mainloop()