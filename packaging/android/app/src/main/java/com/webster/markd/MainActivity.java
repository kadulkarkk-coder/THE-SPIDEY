package com.webster.markd;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ScrollView;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.util.ArrayList;
import java.util.Locale;

public class MainActivity extends Activity {
    private static final int VOICE_REQUEST = 1001;
    private static final int CAMERA_REQUEST = 1002;
    private TextView chat;
    private TextView status;
    private EditText input;
    private ScrollView scroll;
    private PyObject bridge;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        chat = findViewById(R.id.chat);
        status = findViewById(R.id.status);
        input = findViewById(R.id.input);
        scroll = findViewById(R.id.chat_scroll);

        if (!Python.isStarted()) Python.start(new AndroidPlatform(this));
        try {
            bridge = Python.getInstance().getModule("android_bridge");
            String result = bridge.callAttr("bootstrap").toString();
            append("WEBSTER", "Online. " + result);
        } catch (Exception error) {
            status.setText("● DEGRADED");
            append("WEBSTER", "Startup error: " + error.getMessage());
        }

        ((Button) findViewById(R.id.send)).setOnClickListener(v -> sendText());
        input.setOnEditorActionListener((v, actionId, event) -> { sendText(); return true; });
        ((Button) findViewById(R.id.voice)).setOnClickListener(v -> startVoice());
        ((Button) findViewById(R.id.camera)).setOnClickListener(v -> startCamera());
        ((Button) findViewById(R.id.system)).setOnClickListener(v -> showSystem());
    }

    private void sendText() {
        String text = input.getText().toString().trim();
        if (text.isEmpty() || bridge == null) return;
        input.setText("");
        append("YOU", text);
        new Thread(() -> {
            try {
                String result = bridge.callAttr("command", text).toString();
                runOnUiThread(() -> append("WEBSTER", result));
            } catch (Exception error) {
                runOnUiThread(() -> append("WEBSTER", "Error: " + error.getMessage()));
            }
        }).start();
    }

    private void startVoice() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.getDefault());
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Speak to WEBSTER");
        try { startActivityForResult(intent, VOICE_REQUEST); }
        catch (Exception error) { append("WEBSTER", "Voice recognition is unavailable on this device."); }
    }

    private void startCamera() {
        Intent intent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        try {
            startActivityForResult(intent, CAMERA_REQUEST);
            append("WEBSTER", "Camera opened. Vision processing remains on-demand.");
        } catch (Exception error) {
            append("WEBSTER", "Camera is unavailable on this device.");
        }
    }

    private void showSystem() {
        append("WEBSTER", "MARK D\nLocal-first: ready\nOffline core: enabled\nRemote actions: permission controlled\nEvolution: validated plugins\nGesture: disabled on Android\nCamera: on demand\nVoice: on demand");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == VOICE_REQUEST && resultCode == RESULT_OK && data != null) {
            ArrayList<String> results = data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if (results != null && !results.isEmpty()) {
                input.setText(results.get(0));
                sendText();
            }
        } else if (requestCode == CAMERA_REQUEST && resultCode == RESULT_OK) {
            append("WEBSTER", "Image captured. The vision subsystem is available for on-demand analysis.");
        }
    }

    private void append(String speaker, String text) {
        chat.append(speaker + " › " + text + "\n\n");
        scroll.post(() -> scroll.fullScroll(View.FOCUS_DOWN));
    }
}
