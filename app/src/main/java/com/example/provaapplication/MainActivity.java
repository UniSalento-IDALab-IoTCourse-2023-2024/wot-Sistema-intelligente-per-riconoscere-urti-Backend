package com.example.provaapplication;

import android.annotation.SuppressLint;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements SensorEventListener {

    private static final String BROKER_URL = "tcp://test.mosquitto.org:1883";
    private static final String CLIENT_ID = "client_android_12345";
    private static final String USER_ID = "user_12345"; // Aggiungi user_id

    private SensorManager sensorManager;
    private Sensor accelerometer;
    private Sensor gyroscope;
    private TextView accelerometerTextView;
    private TextView gyroscopeTextView;
    private MqttHandler mqttHandler;

    private float[] lastAccelerometerValues = new float[3];
    private float[] lastGyroscopeValues = new float[3];
    private static final float THRESHOLD = 0.05f;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Initialize SensorManager and sensors
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        accelerometerTextView = findViewById(R.id.accelerometerTextView);
        gyroscopeTextView = findViewById(R.id.gyroscopeTextView);

        // Initialize MqttHandler
        mqttHandler = new MqttHandler();
        mqttHandler.connect(BROKER_URL, CLIENT_ID);

        // Initialize last values with Float.MAX_VALUE to ensure the first change is detected
        for (int i = 0; i < 3; i++) {
            lastAccelerometerValues[i] = Float.MAX_VALUE;
            lastGyroscopeValues[i] = Float.MAX_VALUE;
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        // Register the sensor listeners
        sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        sensorManager.registerListener(this, gyroscope, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    protected void onPause() {
        super.onPause();
        // Unregister the sensor listeners
        sensorManager.unregisterListener(this);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            float x = event.values[0];
            float y = event.values[1];
            float z = event.values[2];

            if (hasSignificantChange(lastAccelerometerValues, x, y, z)) {
                lastAccelerometerValues[0] = x;
                lastAccelerometerValues[1] = y;
                lastAccelerometerValues[2] = z;

                String accelerometerData = "Accelerometer\nX: " + x + "\nY: " + y + "\nZ: " + z;
                accelerometerTextView.setText(accelerometerData);
                publishMessage("iot/accelerometer", accelerometerData);
            }
        } else if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
            float x = event.values[0];
            float y = event.values[1];
            float z = event.values[2];

            if (hasSignificantChange(lastGyroscopeValues, x, y, z)) {
                lastGyroscopeValues[0] = x;
                lastGyroscopeValues[1] = y;
                lastGyroscopeValues[2] = z;

                String gyroscopeData = "Gyroscope\nX: " + x + "\nY: " + y + "\nZ: " + z;
                gyroscopeTextView.setText(gyroscopeData);
                publishMessage("iot/gyroscope", gyroscopeData);
            }
        }
    }

    @Override
    protected void onDestroy() {
        if (mqttHandler != null) {
            mqttHandler.disconnect();
        }
        super.onDestroy();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Not necessary for this example
    }

    private boolean hasSignificantChange(float[] lastValues, float x, float y, float z) {
        return Math.abs(lastValues[0] - x) > THRESHOLD ||
                Math.abs(lastValues[1] - y) > THRESHOLD ||
                Math.abs(lastValues[2] - z) > THRESHOLD;
    }

    private void publishMessage(String topic, String message) {
        String messageWithUserId = "user_id: " + USER_ID + "\n" + message;
        mqttHandler.publish(topic, messageWithUserId);
    }
}
