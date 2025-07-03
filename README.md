# ASAChatApplication

Project Description: Our project implements a distributed chat system using a client-server architecture with a dynamically managed server cluster. It features dynamic host discovery, crash fault tolerance, and automatic leader election. Clients connect to the current leader server, which coordinates message exchange and ensures availability by seamlessly handling server failures through automatic role reassignment.
For execution use the following commands: python server.py
python client.py
