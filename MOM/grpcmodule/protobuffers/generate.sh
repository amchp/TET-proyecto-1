#Replication.proto
python -m grpc_tools.protoc -I .  --python_out=../generated/replication/  --pyi_out=../generated/replication/ --grpc_python_out=../generated/replication/ Replication.proto