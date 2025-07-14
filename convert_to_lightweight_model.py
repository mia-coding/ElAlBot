import tensorflow as tf

# Load your trained Keras model
model = tf.keras.models.load_model('chatbot_model.keras')

# Convert to TensorFlow Lite with INT8 quantization
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS,
    tf.lite.OpsSet.SELECT_TF_OPS # Enable if you have custom ops not in TFLite
]
tflite_model = converter.convert()

# Save the TFLite model
with open('chatbot_model.tflite', 'wb') as f:
    f.write(tflite_model)
