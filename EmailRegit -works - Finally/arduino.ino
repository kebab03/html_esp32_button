

const char* ssid = "Wokwi-GUEST";
const char* password = "";

#include <ArduinoJson.h>
#include <vector>
#include <WiFi.h>
#include <HTTPClient.h>



const String url = "http://151.49.22.219/state";
String payload;

const int maxButtonLabels = 15; // Adjust if you have more buttons
char buttonNames[maxButtonLabels][20];
char buttonStates[maxButtonLabels][5];
int buttonPins[maxButtonLabels] = {2, 5, 12, 14, 15, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33};

void fetchJsonData() {
  Serial.print("Fetching " + url + "... ");

  HTTPClient http;
  http.begin(url);

  int httpResponseCode = http.GET();
  if (httpResponseCode > 0) {
    Serial.print("HTTP ");
    Serial.println(httpResponseCode);
    payload = http.getString();
    Serial.println("-----payload-------");
    Serial.println(payload);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
    Serial.println(":-(");
  }

  http.end();
}

StaticJsonDocument<512> doc;

void initiate() {
  fetchJsonData();

  DeserializationError error = deserializeJson(doc, payload);

  JsonArray buttons = doc["buttons"];
  int buttonCount = buttons.size(); // Use int instead of pointer to store the button count
  Serial.print("number of buttons");
  Serial.println(buttonCount);

  // Set up pin mapping for each button
  // Remove this line --> int buttonPins[15] = {2, 5, 12, 14, 15, 18, 19, 21, 22, 23, 25, 26, 27, 32, 33};

  // Store the names and states of the buttons
  for (int i = 0; i < buttonCount; i++) {
    JsonObject button = buttons[i];
    Serial.print("button===");
    Serial.println(button);
    int id = button["id"];
    const char* buttonLabel = button["buttonLabel"];
    const char* state = button["state"];

    // Store the button name and state in the respective arrays
    strncpy(buttonNames[id], buttonLabel, sizeof(buttonNames[id]) - 1);
    strncpy(buttonStates[id], state, sizeof(buttonStates[id]) - 1);
  }

  // Set pin modes for buttons as OUTPUT
  for (int i = 0; i < buttonCount; i++) {
    pinMode(buttonPins[i], OUTPUT);
    Serial.print(buttonNames[i]);
    Serial.print(" is @ pin ");
    Serial.println(buttonPins[i]);
  }
}

void setup() {
  Serial.begin(9600);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("OK! IP=");
  Serial.println(WiFi.localIP());

  delay(100);
}

void loop() {
  initiate();
sendButtonState();
  DeserializationError error = deserializeJson(doc, payload);

  // Read the buttons and perform corresponding actions
  JsonArray buttons = doc["buttons"];

  Serial.print("______-----in loop-----buttons ===============");
  Serial.println(buttons);

  int i = 0;
  for (JsonVariant button : buttons) {
    const char* label = button["buttonLabel"];
    const char* state = button["state"];

    Serial.print("buttonLabel: ");
    Serial.print(label);
    Serial.print(" is @ pin: ");
    Serial.print(buttonPins[i]);
    Serial.print(" in loop and the state is: ");
    Serial.println(state);

    // If the state is "on"
    if (strcmp(state, "on") == 0) {
      // Turn on the corresponding pin
      digitalWrite(buttonPins[i], HIGH);
      Serial.println("is High");
    } else {
      // Turn off the corresponding pin
      digitalWrite(buttonPins[i], LOW);
      Serial.println("is Low");
    }
    i++;
  }

  delay(5000); // Adjust the delay as needed
}


void sendButtonState() {

StaticJsonDocument<256> jsonPayload;
  jsonPayload["key1"] = "value1";
  jsonPayload["key2"] = "value2";
  jsonPayload["key3"] = "value3";

  // Serialize the JSON payload to a string
  String jsonStr;
  serializeJson(jsonPayload, jsonStr);

  // Send the HTTP POST request
  HTTPClient http;
  http.begin("http://151.49.22.219/Pstate");
  http.addHeader("Content-Type", "application/json");
  
  int httpResponseCode = http.POST(jsonStr);
  if (httpResponseCode > 0) {
    Serial.print("HTTP POST request sent. Response code: ");
    Serial.println(httpResponseCode);

    String response = http.getString();
    Serial.print("Response: of http  post------------------");
    Serial.println(response);
  } else {
    Serial.print("Error sending HTTP POST request. Response code: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();  
  
  }
void sendButtonStateP(int buttonId, const char* state, const char* buttonLabel, int buttonPin) {
  HTTPClient http;
  http.begin("http://your-server-address/Pstate");

  // Create a JSON payload with the button information
  StaticJsonDocument<128> doc;
  doc["buttonId"] = buttonId;
  doc["state"] = state;
  doc["buttonLabel"] = buttonLabel;
  doc["buttonPin"] = buttonPin;

  // Serialize the JSON document to a string
  String payload;
  serializeJson(doc, payload);

  // Send the POST request with the payload
  int httpResponseCode = http.POST(payload);
  if (httpResponseCode > 0) {
    Serial.print("HTTP ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}