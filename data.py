import os
import zmq


def fetch_env_data():
    # Fetch comma-separated fields from the environment variable
    prompt_fields_env = os.getenv("prompt_fields", "")
    fields = [field.strip() for field in prompt_fields_env.split(",") if field.strip()]
    sessionId = os.getenv("sessionId", "")

    # Fetch the message environment variable
    message = os.getenv("message", "")

    return fields, message, sessionId


def send_message(fields, message):
    # Prepare ZeroMQ context and PUSH socket
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")  # Adjust address as needed

    # Construct data payload
    data_payload = {"fields": fields, "message": message, "sessionId": sessionId}

    # Send the data payload as a JSON string
    socket.send_json(data_payload)
    print("Message sent:", data_payload)

    reply = socket.recv_json()
    print("Received reply:", reply)


if __name__ == "__main__":
    fields, message, sessionId = fetch_env_data()
    send_message(fields, message)
