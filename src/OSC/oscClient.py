from pythonosc.udp_client import SimpleUDPClient

ip = "YOUR IP"
port = 8000

client = SimpleUDPClient(ip, port)  # Create client

client.send_message("/some/address", 123)   # Send float message
client.send_message("/some/address", [1, 2., "hello"])  # Send message with int, float and string