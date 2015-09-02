set -x

APP_ID=QPdzQHpNzJuUBQlxIYbyFZSQ1pnwMZhT0KfxRZZx
CLIENT_KEY=qdllbVIgjfVK4VivaaiOklH3fl73A5XxUqYBeJzr

cordova plugin remove com.cordova.parseplugin
cordova platform remove android 
cordova platform remove ios 
cordova platform add android 
cordova platform add ios 
rm -rf platforms/android/libs/android-support-v4.jar
cordova plugin add ../../parse-custom --variable APP_ID=${APP_ID} --variable CLIENT_KEY=${CLIENT_KEY}
cordova build ios
python3 setup_parse.py ${APP_ID} ${CLIENT_KEY}
cordova run android
