#! /env/bin/python3
import re
import sys


def run(app_id, client_key):
    txt = ''

    with open('config.xml', 'r', encoding='utf-8') as io:
        txt = ' '.join(io.readlines())
        print(type(txt))

    xid = re.search('id="(.+?)"', txt)
    rawid = xid.group(0)
    cleanid = rawid.replace('id="', '').replace('"', '')
    print(rawid)

    path = cleanid.split('.')
    path = '/'.join(path)
    template = '''package %s;

    import android.app.Application;
    import com.parse.Parse;
    import com.parse.ParseInstallation;

    public class MainApplication extends Application {
        @Override
        public void onCreate() {
            super.onCreate();
            Parse.initialize(this, "%s", "%s");
            ParseInstallation.getCurrentInstallation().saveInBackground();
        }
    }''' % (cleanid, app_id, client_key)

    # print(template)

    with open('platforms/android/src/' + path + '/MainApplication.java', 'w', encoding='utf-8') as io:
        io.write(template + '\n')

    androidManifest = ''
    with open('platforms/android/AndroidManifest.xml', 'r', encoding='utf-8') as io:
        androidManifest = '$$$$'.join(io.readlines())
        androidManifest = androidManifest.replace('<application', '<application android:name="MainApplication"')
        receiver = '        <receiver android:name="com.parse.ParseBroadcastReceiver">$$$$            <intent-filter>$$$$                <action android:name="android.intent.action.BOOT_COMPLETED" />$$$$                <action android:name="android.intent.action.USER_PRESENT" />$$$$            </intent-filter>$$$$        </receiver>$$$$    </application>'
        androidManifest = androidManifest.replace('</application>', receiver)
        # print(androidManifest)

    with open('platforms/android/AndroidManifest.xml', 'w', encoding='utf-8') as io:
        io.writelines(androidManifest.split('$$$$'))

if __name__ == '__main__':
    run(app_id=sys.argv[1], client_key=sys.argv[2])
