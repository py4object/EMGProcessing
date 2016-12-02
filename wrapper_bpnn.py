import os
import time
import datetime
import numpy as np
import bpnn as NN
import progressbar


class WrapperBPNN:

    def __init__(self):
        self.init_network()

    def test_network(self, test_data):
        start_time = time.time()
        print "Raw classification result"
        self.nn.test(test_data)
        elapsed_time = time.time() - start_time
        print "Net classification result w/ threshold"
        for data in test_data:
            print ('----->', self.threshold(self.nn.update(data[0])))
        print "Time elapsed druing classifying: {0}".format(elapsed_time)

    def init_network(self):
        # TODO: Init NN dynamically (accord. to data training lengths)
        try:
            self.training_data = self.get_training_data()
            self.nn = NN.NN(self.ni, self.nh, self.no)
            if(self.load_network()):
                self.nwstatus = "Loaded"
            else:
                print "Load function could NOT be used,RANDOMLY GENERATING NEURAL NETWORK"
                self.nn.__init__(self.ni, self.nh, self.no)
        except Exception as e:
            print "Unexpected error at init_network: ", e
            return False

    def get_training_data(self, path="samples/", reg="fq"):
        print "Getting training data from: ", path
        begin = 0
        end = 74
        step = 1
        ninput = 0
        for i in range(end):
            if i % step == 0:
                ninput += 1
        try:
            movs = os.listdir(path)
            num_movement = len(movs)
            self.ni = ninput
            self.no = num_movement
            self.nh = ninput + 2
            eye = np.eye(num_movement)

            data = []
            for i in range(len(movs)):
                dirpath = path + "/" + movs[i] + "/"
                samples = os.listdir(dirpath)
                for j in range(len(samples)):
                    try:
                        if reg in samples[j]:
                            spath = dirpath + "/" + samples[j]
                            sdata = np.loadtxt(fname=spath)
                            data.append([sdata[begin:end:step], eye[i]])
                    except Exception as e:
                            print (e)
                            print (samples[j])
            return data
        except Exception as e:
            print "Unexpected error:", e

        else:
            print "Training data Successfully loaded"

    def train_network(self, epoch=1000, lr=0.01):
        try:
            training_data = self.training_data
            start = time.time()
            print "Training network in progress"
            bar = progressbar.ProgressBar(maxval=epoch, widgets=[progressbar.Bar(
                '=', '[', ']'), ' ', progressbar.Percentage()])
            bar.start()
            for i in range(epoch):
                self.nn.train(training_data, 1, lr)
                bar.update(i + 1)
            bar.finish()
            elapsed_time = time.time() - start
            print "Epoch: {0}, Time elapsed: {1}".format(epoch, elapsed_time)
        except Exception as e:
            print "Unexpected error:", e
        else:
            return True

    def save_network(self, path="saves/nwstatus/"):
        try:
            dt = datetime.datetime.now()
            # TODO: create folders if they dont exist.
            history_path = path + "old/"
            latest_path = path + "latest/"
            # store current status in a HISTORY folder called OLD that stores all
            # of the past training data
            fwi_old = history_path + self.gen_filename_dtnow("wi", dtnow=dt)
            fwo_old = history_path + self.gen_filename_dtnow("wo", dtnow=dt)
            np.savetxt(fwi_old, self.nn.wi)
            np.savetxt(fwo_old, self.nn.wo)
            # store the current status in LATEST folder - load function will load
            # files from that directory
            fnn_size = np.array([self.ni, self.nh, self.no])
            fnn_new = latest_path + self.gen_filename("nsize")
            np.savetxt(fnn_new, fnn_size)
            fwi_new = latest_path + self.gen_filename("wi")
            fwo_new = latest_path + self.gen_filename("wo")
            np.savetxt(fwi_new, self.nn.wi)
            np.savetxt(fwo_new, self.nn.wo)
        except Exception as e:
            print "Unexpected error:", e
        else:
            print "Successfully saved network status!. See them on: " + path
            return True

    def load_network(self, path="saves/nwstatus/latest/"):
        try:
            # TODO: In case of using __init__; consider it handling in the init_network method. So else would be removed, then ex returns false then according to the result call init in super method.
            # loads the newest save files from saves/nwstatus/latest/
            if os.path.exists(path + "wi.txt") and os.path.exists(path + "wo.txt") and os.path.exists(path + "nsize.txt"):
                ni, nh, no = np.loadtxt(fname=path + "nsize.txt")
                if [ni, nh, no] != [self.ni, self.nh, self.no]:
                    raise Exception(
                        "Load file dimensions DOES NOT match with the current neural network dimensions.")
                # TODO: Check the size of save data if not equal init randomly
                # compare loadedtxt sizes with the sizes that get_training_data
                # func. provides
                print "Save files found: " + path + "wi & wo.txt"
                self.nn.wi = np.loadtxt(fname=path + "wi.txt")
                self.nn.wo = np.loadtxt(fname=path + "wo.txt")
                print "Successfully loaded network status from saves/nwstatus/latest."
                return True
            else:
                raise Exception("Save file(s) missing.")
        except Exception as e:
            print "Unexpected error: ", e
            return False

    def clear(self):
        pass

    def print_nn(self):
        print "**Printing network features**"
        print "Ninp: {0}, Nhid: {1}, Nout: {2}".format(self.nn.ni, self.nn.nh, self.nn.no)
        print "Input Weights:\n{0}".format(self.nn.wi)
        print "Output Weights:\n{0}".format(self.nn.wo)
        print "Network status: {0}".format(self.nwstatus)

    def greater(self, val, limit):
        if val >= limit:
            return 1
        else:
            return 0

    def threshold(self, arr, limit=0.5):
        result = [self.greater(i, limit) for i in arr]
        return result

    def gen_filename_dtnow(self, filename="file", ext="txt", dtnow=datetime.datetime.now()):
        dt = dtnow
        res = str(dt).replace(':', '-').\
            replace(' ', '_').replace('.', '-') + \
            "_" + filename + "." + str(ext)
        return res

    def gen_filename(self, filename="file", ext="txt"):
        res = filename + "." + ext
        return res


if __name__ == '__main__':
    wrp = WrapperBPNN()
    # TODO: Write a function for load training data into arrays
    down = np.loadtxt(fname="test/2016-12-02-03-15-13_CLOSE.fq")
    up = np.loadtxt(fname="test/2016-12-02-03-16-47_OPEN.fq")
    # open3 = np.loadtxt(fname="test/open3.txtfq")
    begin, end, step = 0,74,1
    d1 = down[begin:end:step]
    u1 = up[begin:end:step]
    # o3 = open3[begin:end:step]

    actual_test_data = [
        [d1],
        [u1]
        # ,    [o3]
    ]

    wrp.train_network(epoch=100000)
    wrp.test_network(actual_test_data)
    wrp.save_network()
    # print wrp.training_data
