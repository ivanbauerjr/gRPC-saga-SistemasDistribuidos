### Gerar os arquivos gRPC:
```sh
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. travel.proto
```

### Executar os servidores em terminais separados:
```sh
python server_airline.py
python server_hotel.py
python server_car-rental.py
python travel_agency.py
```

### Rodar o cliente:
```sh
python client.py
```
