![Third](https://github.com/RamonGilabert/Python/blob/master/Resources/third.png)

The third project will use parts of the second project to build the website and have it up and running. It will be basically a system where you can go with an NFC phone and make the Raspberry Pi read the temperature sensor, after that, save it to the database and send a notification with a command to say it loud from the command line.

#### Parts of it

- Database storing the temperature, when was it read and the change of temperature. Also one to store Users.
- NFC and Temperature sensors that will have their own class each.
- Notifications, fully configurable to add more if needed.
- Some tests when it makes sense.

#### Considerations

##### Notifications

From the configuration file you'll be able to add which outputs you want, using the library pyttsx we are going to output the voice. Note that there are some problems using the library in OS X Yosemite and El Capitan, that's why initially, the configuration file adds a False in the initialization of the voice.

##### Database

The database has two major tables, Users and Temperatures, one storing **Name** and **NFC**, since we are not going to use Telegram in here. A part from that, there's the Temperatures table that will hold the values **Initial temperature**, **Date**, **Difference** and **NFC**, that is to create a relation between tables.

##### Sensors

As for now, everything is mocked, thing that will change a bit later. The NFC reader returns a person with the same username and NFC values in a random form. The THSensor returns a random temperature. When implementing, this will change.

##### Source

There's a website (with an image above) that will represent the temperatures when any. It has also an empty state.

##### Tests

I added one test that checks if the Text broadcaster works as it should, I'll try to keep adding more and more when it makes sense. Tests are my weakness at work too, that's why I kind of need to get better at it.
