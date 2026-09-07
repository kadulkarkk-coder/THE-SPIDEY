package com.webster.markd;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView status = findViewById(R.id.status);
        status.setText("Starting WEBSTER...");

        if (!Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }

        try {
            PyObject bridge = Python.getInstance().getModule("android_bridge");
            PyObject result = bridge.callAttr("bootstrap");
            status.setText("WEBSTER is ready\n" + result.toString());
        } catch (Exception error) {
            status.setText("WEBSTER startup error\n" + error.getMessage());
        }
    }
}
