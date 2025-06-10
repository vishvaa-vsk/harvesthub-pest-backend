"""
Model service for handling ML predictions
"""
import asyncio
import os
import tensorflow as tf
import numpy as np
from PIL import Image
from datetime import datetime
from typing import Optional, Dict, Any, IO
from io import BytesIO

from app.core.config import settings
from app.core.exceptions import ModelException


class ModelService:
    """Service for handling machine learning model operations"""
    
    _instance = None
    _model = None
    _labels = []
    
    def __new__(cls):
        """Singleton pattern to ensure only one model instance"""
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._initialize_model()
        return cls._instance
    
    def _initialize_model(self):
        """Initialize the model and labels"""
        self._load_model()
        self._load_labels()
    
    def _load_model(self):
        """Load TensorFlow model with optimized settings for consistent predictions"""
        try:
            if os.path.exists(settings.MODEL_PATH):
                # Set random seeds for deterministic behavior
                tf.random.set_seed(42)
                np.random.seed(42)
                
                # Configure TensorFlow for deterministic behavior
                tf.config.threading.set_intra_op_parallelism_threads(1)
                tf.config.threading.set_inter_op_parallelism_threads(1)
                
                # Enable deterministic ops
                tf.config.experimental.enable_op_determinism()
                
                # Load model with explicit configurations
                self._model = tf.keras.models.load_model(
                    settings.MODEL_PATH,
                    compile=False  # Don't compile to avoid optimizer state issues
                )
                
                # Recompile with consistent settings
                self._model.compile(
                    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                    loss='categorical_crossentropy',
                    metrics=['accuracy']
                )
                
                print(f"✅ Model loaded from {settings.MODEL_PATH}")
                print(f"   Input shape: {self._model.input_shape}")
                print(f"   Output shape: {self._model.output_shape}")
            else:
                print(f"⚠️  Model file not found at {settings.MODEL_PATH}, creating dummy model")
                self._model = self._create_dummy_model()
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self._model = self._create_dummy_model()
    
    def _create_dummy_model(self):
        """Create a dummy model for testing"""
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(224, 224, 3)),
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(66, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def _load_labels(self):
        """Load class labels"""
        try:
            if os.path.exists(settings.LABELS_PATH):
                with open(settings.LABELS_PATH, 'r') as f:
                    self._labels = [line.strip() for line in f.readlines()]
                print(f"✅ Labels loaded: {len(self._labels)} classes")
            else:
                print(f"⚠️  Labels file not found at {settings.LABELS_PATH}")
                self._labels = [f"class_{i}" for i in range(66)]
        except Exception as e:
            print(f"❌ Error loading labels: {e}")
            self._labels = [f"class_{i}" for i in range(66)]
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._model is not None
    
    def get_labels_count(self) -> int:
        """Get number of labels"""
        return len(self._labels)
    
    def get_labels(self) -> list:
        """Get all labels"""
        return self._labels
    
    def _preprocess_image(self, image_file: IO[bytes]) -> Optional[np.ndarray]:
        """Preprocess image for model prediction with consistent normalization"""
        try:
            # Reset file pointer to beginning
            image_file.seek(0)
            
            # Open and process image
            image = Image.open(image_file)
            image = image.convert('RGB')
            
            # Resize with high-quality resampling for consistency
            image = image.resize(settings.IMAGE_SIZE, Image.Resampling.LANCZOS)
            
            # Convert to numpy array with consistent dtype
            image_array = np.array(image, dtype=np.float32)
            
            # Normalize to [0,1] range consistently
            image_array = image_array / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            # Ensure consistent shape
            assert image_array.shape == (1, 224, 224, 3), f"Unexpected shape: {image_array.shape}"
            
            return image_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def predict(self, image_file: IO[bytes]) -> Optional[Dict[str, Any]]:
        """Make prediction on image with consistent confidence calculation"""
        if not self.is_model_loaded():
            return None
        
        try:
            processed_image = self._preprocess_image(image_file)
            if processed_image is None:
                return None
            
            # Make prediction with consistent settings
            with tf.device('/CPU:0'):  # Force CPU for consistency
                predictions = self._model.predict(
                    processed_image, 
                    batch_size=1,
                    verbose=0
                )
            
            # Get prediction results
            predicted_index = int(np.argmax(predictions[0]))
            confidence = float(predictions[0][predicted_index])
            
            # Ensure confidence is within valid range
            confidence = max(0.0, min(1.0, confidence))
            
            # Get label
            label = self._labels[predicted_index] if predicted_index < len(self._labels) else f"class_{predicted_index}"
            
            # Log prediction for debugging
            print(f"Prediction - Label: {label}, Confidence: {confidence:.4f}, Index: {predicted_index}")
            
            return {
                'label': label,
                'confidence': confidence,
                'index': predicted_index,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    
    async def initialize(self):
        """Async initialization"""
        if not self.is_model_loaded():
            self._initialize_model()
    
    def get_total_classes(self) -> int:
        """Get total number of classes"""
        return len(self._labels)
    
    async def predict_async(self, image_file: IO[bytes]) -> Optional[Dict[str, Any]]:
        """Async prediction wrapper"""
        return self.predict(image_file)
