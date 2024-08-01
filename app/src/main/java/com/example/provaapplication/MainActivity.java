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

    private SensorManager sensorManager;
    private Sensor accelerometer;
    private Sensor gyroscope;
    private TextView accelerometerTextView;
    private TextView gyroscopeTextView;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Ottieni il riferimento al SensorManager
        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        // Ottieni il riferimento all'accelerometro
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        accelerometerTextView = findViewById(R.id.accelerometerTextView);

        // Ottieni il riferimento al giroscopio
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
        gyroscopeTextView = findViewById(R.id.gyroscopeTextView);
    }

    @Override
    protected void onResume() {
        super.onResume();
        // Registra il listener per l'accelerometro e il giroscopio
        sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_NORMAL);
        sensorManager.registerListener(this, gyroscope, SensorManager.SENSOR_DELAY_NORMAL);
    }

    @Override
    protected void onPause() {
        super.onPause();
        // Deregistra il listener per l'accelerometro e il giroscopio
        sensorManager.unregisterListener(this);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        // Gestisci i dati dell'accelerometro
        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            float x = event.values[0];
            float y = event.values[1];
            float z = event.values[2];
            String accelerometerData = "Accelerometer\nX: " + x + "\nY: " + y + "\nZ: " + z;
            accelerometerTextView.setText(accelerometerData);
        }

        // Gestisci i dati del giroscopio
        if (event.sensor.getType() == Sensor.TYPE_GYROSCOPE) {
            float x = event.values[0];
            float y = event.values[1];
            float z = event.values[2];
            String gyroscopeData = "Gyroscope\nX: " + x + "\nY: " + y + "\nZ: " + z;
            gyroscopeTextView.setText(gyroscopeData);
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // Non necessario per questo esempio
    }
}


