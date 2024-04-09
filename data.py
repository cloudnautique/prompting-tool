import os
import zmq
import json


def fetch_env_data():
    # Fetch comma-separated fields from the environment variable
    prompt_fields_env = os.getenv("prompt_fields", "")
    fields = [field.strip() for field in prompt_fields_env.split(",") if field.strip()]
    sessionId = os.getenv("sessionId", "")
    msg_type = os.getenv("messageType", "message")

    # Fetch the message environment variable
    message = os.getenv("message", "")

    return fields, message, sessionId, msg_type


def send_message(fields, message, sessionId, msg_type="message"):
    # Prepare ZeroMQ context and PUSH socket
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect("tcp://localhost:5555")  # Adjust address as needed

    # Construct data payload
    data_payload = {
        "type": msg_type,
        "fields": fields,
        "message": message,
        "sessionId": sessionId,
    }

    # Send the data payload as a JSON string
    print(data_payload)
    json_data=json.dumps(data_payload).encode('utf-8')
    socket.send(json_data)
    print("Message sent:", data_payload)

    print("waiting for reply")
    reply = socket.recv_json()
    print("Received reply:", reply)


if __name__ == "__main__":
    fields, message, sessionId, msg_type = fetch_env_data()
    send_message(fields, message, sessionId, msg_type)
