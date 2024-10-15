import sys
import json
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
import os

load_dotenv()

# Workaround for Python 3.12+ compatibility with kafka-python library
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

import socket
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Initialize Kafka producer with connection details
producer = KafkaProducer(
    bootstrap_servers=os.getenv('KAFKA_URL'),
    security_protocol="SASL_SSL",
    sasl_mechanism="SCRAM-SHA-256",
    sasl_plain_username=os.getenv('KAFKA_USERNAME'),
    sasl_plain_password=os.getenv('KAFKA_PASSWORD'),
)
# Get the hostname to use as the message key
hostname = str.encode(socket.gethostname())

# Callback function for successful message sending
def on_success(metadata):
    print(f"Sent to topic '{metadata.topic}' at offset {metadata.offset}")

# Callback function for error handling
def on_error(e):
    print(f"Error sending message: {e}")

# Sample dataset of comments with their IDs and harmfulness labels
comments_with_labels = [
    (1, "This is a friendly comment", False),
    (2, "You're an idiot", True),
    (3, "Great post, thanks for sharing!", False),
    (4, "I hope you die", True),
    (5, "Your analysis is spot on, I learned a lot", False),
    (6, "This article is garbage", True),
    (7, "I respectfully disagree with your point", False),
    (8, "Go back to where you came from", True),
    (9, "Can you provide more details on this topic?", False),
    (10, "You should be ashamed of yourself", True),
    (11, "I appreciate your perspective on this issue", False),
    (12, "This is fake news, you're a liar", True),
    (13, "Your work has really inspired me", False),
    (14, "I'm going to report you to the authorities", True),
    (15, "Let's agree to disagree on this one", False),
    (16, "You're nothing but a fraud", True),
    (17, "This content is really helpful, thank you", False),
    (18, "I wish you would just disappear", True),
    (19, "I hadn't considered that angle before, interesting", False),
    (20, "You're brainwashed by the media", True),
    (21, "Could you clarify your third point?", False),
    (22, "Stop spreading your propaganda", True),
    (23, "I'm looking forward to your next post", False),
    (24, "You're a disgrace to your profession", True),
    (25, "This discussion has been very enlightening", False),
    (26, "I hope your account gets banned", True),
    (27, "Your research seems very thorough", False),
    (28, "You're just pushing your own agenda", True),
    (29, "I found your arguments very compelling", False),
    (30, "Nobody cares about your opinion", True),
    (31, "This is a complex issue, thanks for breaking it down", False),
    (32, "You're part of the problem in society", True),
    (33, "I'm sharing this with my colleagues", False),
    (34, "Do the world a favor and stop posting", True),
    (35, "Your insights have changed my perspective", False),
    (36, "You're clearly not qualified to discuss this", True),
    (37, "This is a balanced and fair analysis", False),
    (38, "I'm reporting this post for misinformation", True),
    (39, "You've given me a lot to think about", False),
    (40, "Your stupidity is beyond belief", True)
]

# Process each comment in the dataset
for i, (id, comment, is_harmful) in enumerate(comments_with_labels):
    # Initialize the SentenceTransformer model (only once)
    if 'model' not in locals():
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Generate embeddings for the comment
    embeddings = model.encode([comment])[0].tolist()
    
    # Create a JSON object with comment data
    msg = json.dumps({
        "id": id,
        "embeddings": embeddings,
        "is_harmful": is_harmful
    })

    # Send the message to Kafka topic
    future = producer.send(
        "content-ingestor",
        key=hostname,
        value=str.encode(msg)  # Encode the JSON string
    )
    # Add callback functions for success and error handling
    future.add_callback(on_success)
    future.add_errback(on_error)

# Ensure all messages are sent before closing the producer
producer.flush()
producer.close()
