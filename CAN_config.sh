sudo modprobe vcan 
sudo ip link add name vcan0 type vcan 
sudo ip link set dev vcan0 up  
sudo ip link add name vcan1 type vcan 
sudo ip link set dev vcan1 up  
sudo ip link add name vcan2 type vcan 
sudo ip link set dev vcan2 up