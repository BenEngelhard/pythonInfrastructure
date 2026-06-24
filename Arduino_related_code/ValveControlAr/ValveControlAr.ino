// Serial port constants
const int baud_rate = 9600;

// Control constants 
const int ONBOARD_LED          = 13;        // digital out to drive the on board LED for heart bit
const int SLOW_HEART_BIT_DELAY = 500;       // Delay time for slow rate heartbit 
const int FAST_HEART_BIT_DELAY = 200;       // delay time for the fast rate heartbit

// control variables
bool heartBitOn;                            // marks that heart bit LED is currently on
int  heartBitDelay;
int  digitalPinMode[NUM_DIGITAL_PINS];      // keeps track of channel mode. 0 - input, 1 - output
int  pulseWidth[NUM_DIGITAL_PINS];          // Keeps track of required pulse widths
int  pulsePolarity[NUM_DIGITAL_PINS];       //
unsigned long startTime[NUM_DIGITAL_PINS];  // keeps track of pulse start times.
char command;
int  channel;
int  polarity;
int  messagePart;
unsigned long heartbitTime;
unsigned long messageStart;

// setup code - runs once
void setup() 
{
  // Digital system initialization
  pinMode(ONBOARD_LED, OUTPUT);
  
  // Close all vales
  for (int i = 7; i <= 12; i++)
  {
    pinMode(i, OUTPUT);
    digitalWrite(i, HIGH);
  }

  //temp ben
  //for (int i = 3; i <= 6; i++)
  //{
  //  pinMode(i, OUTPUT);
  //  digitalWrite(i, HIGH);
  //}
  // end temp ben

  // Serial port initialization
  Serial.begin(baud_rate);
  
  // Control Variables initialization
  heartBitOn = false;
  heartBitDelay = SLOW_HEART_BIT_DELAY;
  messagePart = 0; 
  for (int i = 0; i < NUM_DIGITAL_PINS; i++) 
  {
    digitalPinMode[i] = 0; 
    startTime[i] = 0;
  }
  heartbitTime = millis();
  messageStart = 0;
  
  // blink three times to indicate start of program
  digitalWrite(ONBOARD_LED, LOW);
  for (int it = 0; it < 3; it++) 
  {
    digitalWrite(ONBOARD_LED, HIGH);
    delay(100);
    digitalWrite(ONBOARD_LED, LOW);
    delay(100);  
  }
}

// main code, runs repeatedly:
void loop() 
{    
  endPulses();
  if ((messageStart > 0) && (millis() - messageStart > 500))
  {
    twitch(messagePart);
    messagePart = 0;
    messageStart = 0;
  }
  
  switch (messagePart)
  {
    case 0:     // op code       
      if (Serial.available() > 0) 
      {   
        // read a single op code byte
        command = Serial.read();
        if ((command == 'E') || (command == 'P'))
        {
          messageStart = millis();
          messagePart++;
        }
      }
      break;
      
    case 1:     // channel       
      if (Serial.available() > 0) 
      {   
        // read a single pin # byte
        channel = Serial.read();
        messagePart++;
      }
      break;
      
    case 2:     // polarity       
      if (Serial.available() > 0) 
      {   
        // read a single polarity byte
        polarity = Serial.read();
        messagePart++;
      }
      break;

    case 3:     // width       
      if (Serial.available() > 1) 
      {   
        // read two pulse width bytes
        int width = (Serial.read() << 8) + Serial.read();
        messagePart = 0;
        messageStart = 0;
        actOnChannel(command, channel, polarity, width);
      }
      break;
  }  
  performHeartBit();  
}

bool configureChannel(byte digChannel)
{
  bool valid = false;
  if ((digChannel >= 0) && (digChannel < NUM_DIGITAL_PINS))
  {
    valid = true;
    if (digitalPinMode[digChannel] == 0)
    {
        pinMode(digChannel, OUTPUT);
        digitalPinMode[digChannel] = 1; 
    }
  }
  return valid;
}

void actOnChannel(char command, int channel, int polarity, int width)
{
  bool operationValid = false;
  heartBitDelay = FAST_HEART_BIT_DELAY;
  
  if (configureChannel(channel))
  {
    if (command == 'E')
      operationValid = setDigital(channel, polarity);
    if (command == 'P')
      operationValid = startPulse(channel, polarity, width);
  }

  if (operationValid)
    heartBitDelay = SLOW_HEART_BIT_DELAY;
}
      
bool setDigital(int channel, int polarity)
{      
  bool operationValid = false;  

  if (polarity == 1)
  {
    digitalWrite(channel, HIGH);
    operationValid = true;
  }
  else if (polarity == 0)
  {
    digitalWrite(channel, LOW);
    operationValid = true;
  }
  return operationValid;
}

bool startPulse(int channel, int polarity, int width)
{
  bool operationValid = false;  
  if (setDigital(channel, polarity))
  { 
     pulseWidth[channel] = width;
     pulsePolarity[channel] = polarity; 
     startTime[channel] = millis();
  }
  return operationValid;
}

void endPulses()
{
  unsigned long currentTime;
  
  for (int i = 0; i < NUM_DIGITAL_PINS; i++) 
  {
     if (startTime[i] > 0)
     {
       currentTime = millis();
       if (currentTime - startTime[i] > pulseWidth[i])
       {
         startTime[i] = 0;
         int polarity = (pulsePolarity[i] == 1) ? 0 : 1;
         setDigital(i, polarity);     
       }
     }
  }
}
 

void performHeartBit()  
{
  unsigned long currentTime;
  
  currentTime = millis();
  
  if (currentTime - heartbitTime > heartBitDelay)
  {
    if (heartBitOn)
    {
      digitalWrite(ONBOARD_LED, LOW);
      heartBitOn = false;
    }
    else
    {
      digitalWrite(ONBOARD_LED, HIGH);
      heartBitOn = true;
    }
    heartbitTime = currentTime;
  }
}

void twitch(int count)
{
  digitalWrite(ONBOARD_LED, LOW);
  for (int tc = 0; tc < count; tc++)
  {
    for (int it = 0; it < 2; it++) 
    {
      digitalWrite(ONBOARD_LED, HIGH);
      delay(50);
      digitalWrite(ONBOARD_LED, LOW);
      delay(50);  
    }
    delay (200);
  }
}

