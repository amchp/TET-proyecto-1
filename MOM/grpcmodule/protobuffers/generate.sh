#Replication.proto
python -m grpc_tools.protoc -I .  --python_out=../generated/replication/  --pyi_out=../generated/replication/ --grpc_python_out=../generated/replication/ Replication.proto
#Update.proto
python -m grpc_tools.protoc -I .  --python_out=../generated/update/  --pyi_out=../generated/update/ --grpc_python_out=../generated/update/ Update.proto