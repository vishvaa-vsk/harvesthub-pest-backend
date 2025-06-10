import os
import tensorflow as tf
import numpy as np
from datetime import datetime
import tensorflow as tf
import numpy as np
import os
from PIL import Image

class PestDetectionModel:
    def __init__(self):
        self.model = None
        self.labels = []
        self.load_model()
        self.load_labels()

    def load_model(self):
        """Load the TensorFlow/Keras model from .h5 file"""
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'data', 'model.h5')
            if os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
                print(f"Model loaded successfully from {model_path}")
            else:
                print("Model file not found. Creating dummy model for testing.")
                self.model = self._create_dummy_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = self._create_dummy_model()

    def _create_dummy_model(self):
        """Create a dummy model for testing when actual model is not available"""
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(224, 224, 3)),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(len(self.labels) if self.labels else 66, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def load_labels(self):
        """Load class labels from labels.txt file"""
        try:
            labels_path = os.path.join(os.path.dirname(__file__), 'data', 'labels.txt')
            if os.path.exists(labels_path):
                with open(labels_path, 'r', encoding='utf-8') as f:
                    self.labels = [line.strip() for line in f.readlines() if line.strip()]
                print(f"Loaded {len(self.labels)} labels from {labels_path}")
            else:
                print("Labels file not found. Using default labels.")
                self.labels = [f"class_{i}" for i in range(66)]
        except Exception as e:
            print(f"Error loading labels: {e}")
            self.labels = [f"class_{i}" for i in range(66)]

    def preprocess_image(self, image_file):
        """Preprocess the uploaded image for model prediction"""
        try:
            # Open and convert image
            image = Image.open(image_file).convert('RGB')
            
            # Resize to model input size (224x224)
            image = image.resize((224, 224))
            
            # Convert to numpy array and normalize
            image_array = np.array(image, dtype=np.float32)
            image_array = image_array / 255.0  # Normalize to [0,1]
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None

    def predict(self, image_file):
        """Make prediction on the uploaded image"""
        try:
            # Preprocess the image
            preprocessed_image = self.preprocess_image(image_file)
            
            if preprocessed_image is None:
                return None
            
            # Make prediction
            predictions = self.model.predict(preprocessed_image)
            
            # Get the predicted class index and confidence
            predicted_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_index])
            
            # Get the label
            if predicted_index < len(self.labels):
                predicted_label = self.labels[predicted_index]
            else:            predicted_label = f"unknown_class_{predicted_index}"
            
            return {
                "label": predicted_label,
                "confidence": confidence,
                "index": int(predicted_index),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None
