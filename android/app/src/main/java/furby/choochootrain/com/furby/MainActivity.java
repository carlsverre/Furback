package furby.choochootrain.com.furby;

import android.content.*;
import android.os.*;
import android.speech.*;
import android.view.View;
import android.widget.*;
import android.app.*;

import java.io.*;
import java.io.UnsupportedEncodingException;
import java.util.*;
import android.speech.tts.*;
import java.util.Locale;
import java.net.*;

import android.util.*;
import org.apache.http.*;
import org.apache.http.client.*;
import org.apache.http.util.*;
import org.apache.http.client.methods.*;
import org.apache.http.impl.client.*;
import android.media.*;
import android.net.*;


public class MainActivity extends Activity implements TextToSpeech.OnInitListener {
    public static int REQUEST_CODE = 1234;
    public static String URL = "http://192.168.2.133:9000/?text=";
    public static String DEFAULT_RESPONSE = "do 820\ndo 820\ndo 820\ndo 704";
    public static boolean DEBUG = false;
    public TextView speech;
    public TextToSpeech tts;
    public AudioManager audioManager;
    private MediaPlayer mp;
    private Button askFurby;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tts = new TextToSpeech(this, this);
        speech = (TextView) findViewById(R.id.speech);
        askFurby = (Button) findViewById(R.id.call);
        askFurby.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startRecognitionCycle();
                askFurby.setEnabled(false);
            }
        });

        audioManager =(AudioManager)getSystemService(Context.AUDIO_SERVICE);
        mp = new MediaPlayer();
        //audioManager.setStreamMute(AudioManager.STREAM_MUSIC, true);
    }

    private void startRecognitionCycle(){
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        startActivityForResult(intent, REQUEST_CODE);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
            ArrayList<String> matches_text = data
                    .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);
            if (matches_text.size() > 0) {
                speech.setText(matches_text.get(0));
                new ProcessTask().execute(matches_text.get(0));
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    private String sendText(String text) {
        if (DEBUG) return DEFAULT_RESPONSE;
        try {
            String u = URL + URLEncoder.encode(text, "utf-8");
            Log.d("URL", "Going to hit " + u);

            HttpClient client = new DefaultHttpClient();
            HttpGet request = new HttpGet(u);

            HttpResponse response = client.execute(request);
            HttpEntity entity = response.getEntity();
            String content = EntityUtils.toString(entity);

            return content;
        } catch (UnsupportedEncodingException e) {
            Log.e("WTF", "ENCODING UNSUPPORTED");
        } catch (MalformedURLException e) {
            Log.e("WTF", "URL MALFORMED");
        } catch (IOException e) {
            Log.e("WTF", "IO FUCKED");
            e.printStackTrace();
        }

        return DEFAULT_RESPONSE;
    }

    @Override
    protected void onDestroy() {
        if (tts!=null) {
            tts.stop();
            tts.shutdown();
        }

        super.onDestroy();
    }

    public void say(String s) {
        Log.e("SAY", s);

        //audioManager.setStreamMute(AudioManager.STREAM_MUSIC, false);
        this.tts.speak(s, TextToSpeech.QUEUE_FLUSH, null);
        //audioManager.setStreamMute(AudioManager.STREAM_MUSIC, true);
    }

    public void action(int s) {
        Log.e("ACTION", s + ".wav");
        //try {
            //mp.setDataSource("/sdcard/furby/" + s + ".wav");
            //mp.prepare();
            //mp.start();
            //mp.reset();
            Intent intent = new Intent();
            intent.setAction(android.content.Intent.ACTION_VIEW);
            File file = new File("/sdcard/furby/" + s + ".wav");
            intent.setDataAndType(Uri.fromFile(file), "audio/*");
            startActivity(intent);
            pause(2000);
        //} catch (IOException e) {
        //    Log.e("ACTION", "action " + s + " not working");
        //}
    }

    public void pause(float s) {
        try {
            Log.e("WAIT", s + " milliseconds");
            Thread.sleep((long)s);
        } catch (InterruptedException e) {
            Log.e("WAIT", "couldnt wait " + s + " miliseconds");
        }
    }

    @Override
    public void onInit(int status) {
        if (status == TextToSpeech.SUCCESS) {
            tts.setLanguage(Locale.getDefault());
        } else {
            tts= null;
            Toast.makeText(this, "FAILED TTS", Toast.LENGTH_LONG).show();
        }
    }

    public class ProcessTask extends AsyncTask<String, Void, Void> {
        @Override
        protected Void doInBackground(String... params) {
            try {
                String res = sendText(params[0]);
                Log.d("RESPONSE", res);
                if (res != null) {
                    StringTokenizer st = new StringTokenizer(res, "\n");
                    while (st.hasMoreTokens()) {
                        String token = st.nextToken();

                        try {
                            if (token.startsWith("say ")) {
                                say(token.substring(4));
                            } else if (token.startsWith("do ")) {
                                action(Integer.parseInt(token.substring(3)));
                            } else if (token.startsWith("wait ")) {
                                pause(Float.parseFloat(token.substring(5)));
                            } else
                                Log.e("PARSE", token);
                        } catch (Exception e) {
                            e.printStackTrace();
                        }
                    }
                    Log.e("PROCESS", "done.");
                }
            } catch (Exception e) {
                Log.e("WTF", "Error");
                e.printStackTrace();
            }

            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    askFurby.setEnabled(true);
                }
            });

            return null;
        }
    }
}
