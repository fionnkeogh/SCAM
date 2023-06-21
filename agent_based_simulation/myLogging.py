import datetime

class Logger:
    def __init__(self):
        current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.log_path = "log/"+current_time+".log"
        self.log_file = open(self.log_path, "a")

    def __del__(self):
        self.log_file.close()

    def log(self, message):
        self.log_file.write(message)
        self.log_file.write("\n")
    
    def log_state(self, state):
        self.log("STATE:")
        for obj in state:
            self.log(str(obj))
    
    def warning(self, warning):
        self.log("WARNING: "+warning)

    def error(self, error):
        self.log("ERROR: "+error)
