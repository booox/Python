# Main program.

import sys
import threading
import time

sys.path.append('./../')

from sensors.nfcsensor import NFCSensor
from sensors.thsensor import THSensor
from communication.notify import Notify
from source.database.user import User
from source.database.temperature import Temperature
from source.app import app

DATABASE = '/tmp/third.db'

class App(object):

    def __init__(self):
        # TODO: Parse the configuration file and start the program.
        self.nfc_sensor = NFCSensor()
        self.th_sensor = THSensor()
        self.notify = Notify()
        self.user_model = User(DATABASE)
        self.temperature_model = Temperature(DATABASE)

        self._prepare_threads()
        self._main_loop()

    def _prepare_threads(self):
        self.app_thread = threading.Thread(target=self._run_web_app)
        self.app_thread.daemon = True
        self.app_thread.start()

    def _run_web_app(self):
        app.run()

    def _main_loop(self):
        print 'Starting the main loop'

        try:
            while True:
                data = self.nfc_sensor.get_data()
                if data is not None:
                    temperature = self.th_sensor.get_data()
                    date = time.strftime('%d.%m.%Y at %H:%M')

                    self.notify.broadcast(temperature)
                    self.user_model.add(data['name'], data['nfc'])
                    self.temperature_model.add(temperature, date, 2, data['nfc'])

                time.sleep(2) # TODO: Delete this when implementing.
        finally:
            print 'Closing the app.'
