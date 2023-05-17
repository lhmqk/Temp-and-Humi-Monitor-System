package com.example.demoiot;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import android.widget.SeekBar;

import com.github.angads25.toggle.interfaces.OnToggledListener;
import com.github.angads25.toggle.model.ToggleableView;
import com.github.angads25.toggle.widget.LabeledSwitch;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {

    MQTTHelper mqttHelper;
    TextView txtTemp, txtHumid;
    LabeledSwitch btnLED, btnPUMP;
    SeekBar adjBar;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        txtTemp = findViewById(R.id.txtTemperature);
        txtHumid = findViewById(R.id.txtHumidity);
        btnLED = findViewById(R.id.btnLED);
        btnPUMP = findViewById(R.id.btnPUMP);

        btnLED.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn == true){
                    sendDataMQTT("jamewood/feeds/nutnhan1", "1");
                } else {
                    sendDataMQTT("jamewood/feeds/nutnhan1", "0");
                }
            }
        });
        btnPUMP.setOnToggledListener(new OnToggledListener() {
            @Override
            public void onSwitched(ToggleableView toggleableView, boolean isOn) {
                if(isOn == true){
                    sendDataMQTT("jamewood/feeds/nutnhan2", "1");
                } else {
                    sendDataMQTT("jamewood/feeds/nutnhan2", "0");
                }
            }
        });

        adjBar=findViewById(R.id.seekBar);
        adjBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener(){
            int progressChangedValue = 0;

            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                progressChangedValue = progress;
            }

            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }

            public void onStopTrackingTouch(SeekBar seekBar) {
                sendDataMQTT("jamewood/feeds/sending-freq",Integer.toString(progressChangedValue));
                Log.d("TEST",Integer.toString(progressChangedValue));
            }
        });
        adjBar.setMax(30);
        adjBar.setProgress(10);

        startMQTT();
    }

    public void sendDataMQTT(String topic, String value){
        MqttMessage msg = new MqttMessage();
        msg.setId(1234);
        msg.setQos(0);
        msg.setRetained(false);

        byte[] b = value.getBytes(Charset.forName("UTF-8"));
        msg.setPayload(b);

        try {
            mqttHelper.mqttAndroidClient.publish(topic, msg);
        }catch (MqttException e){

        }
    }

    public void startMQTT(){
        mqttHelper = new MQTTHelper(this);
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.d("TEST", topic + "***" + message.toString());
                if(topic.contains("cambien1")){
                    txtTemp.setText(message.toString() + "°C");
                } else if(topic.contains("cambien2")){
                    txtHumid.setText(message.toString() + "%");
                } else if(topic.contains("nutnhan1")){
                    if(message.toString().equals("1")){
                        btnLED.setOn(true);
                    } else {
                        btnLED.setOn(false);
                    }
                } else if(topic.contains("nutnhan2")){
                    if(message.toString().equals("1")){
                        btnPUMP.setOn(true);
                    } else {
                        btnPUMP.setOn(false);
                    }
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}