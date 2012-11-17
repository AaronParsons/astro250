# 
#  fir_filter_udp_rx.py
#  <Script to continuously accept BRAM binary information
#  over a UDP connection and plot them up>
#  
#  Initially created by Isaac Shivvers on 2012-10-12
#  Edited by Nick Hand 
# 
import matplotlib
matplotlib.use('macosx') # problems arise with multiprocessing and other backends (not sure why)

import matplotlib.pyplot as pl
import numpy as np
import struct, socket
import digital_utils, argparse
import multiprocessing as mp

class receiveUDP(object):
    """
    @brief class to receive data from ROACH via UDP using parallel processing
    """
    def __init__(self, timestep=5e-9, dtype='ddc', port=12345):
        """
        @brief set up the UDP connection to receive
        """
        
        self.port            = port     # the port to talk over
        self.dt              = timestep # the timestep of the samples
        self.dtype           = dtype    # the type of data ('ddc' or 'data')
        self.max_recvd_bytes = 2**15    # the maximum bytes to receive per packets
        self.max_to_plot     = 1024      # number of samples to show in plot
        self.show            = 100

    def start(self):
        """
        @brief start receiving data by setting up a multiprocessing Process
        to receive data through a UDP socket and one Process to continuously
        plot the data received
        """
        
        # initialize the Process Manager and shared Process Namespace
        manager = mp.Manager()
        ns = manager.Namespace()
        ns.unseen_samples = np.array([]) # the array to store the samples received

        # use an Event so we don't read from sample array while writing to it
        trig = mp.Event()

        # initialize the Process that will receive data from socket
        p_rcv = mp.Process(target=self.rcv, args=(ns,trig,))
        p_rcv.start()

        # initialize the Process that will plot the data
        p_plot = mp.Process(target=self.continuous_plot, args=(ns,trig, ))
        p_plot.start()

        # run the Processes
        p_rcv.join()
        p_plot.join()


    def rcv(self, ns, trig):
        """
        @brief receive the data from a UDP socket
        
        @param ns: the shared Namespace between the two running Processes
        (multiprocessing.Manager.Namespace)
        @param trig: a trigger event to make sure we don't write/read shared array
        at same time (multiprocessing.Event)
        """
        # set up the socket as UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # always make sure we close the socket if program crashes
        try: 
            # bind the socket to the input port
            sock.bind( ('0.0.0.0', self.port) )
            
            # loop continuously and receive data
            while True:
            
                # read in new data as long as the trig is not set
                if not trig.is_set():
                    
                    # receive the binary data through the socket
                    binary_data = sock.recv(self.max_recvd_bytes)
                    
                    # process the binary data depending on if it is from a ddc_bram or data_bram file
                    if self.dtype == 'ddc':
                        times, newdata = digital_utils.process_ddc_bram(None, timestep=self.dt, data=binary_data)
                    else:
                        times, newdata = digital_utils.process_data_bram(None, timestep=self.dt, data=binary_data)
                        
                    # concatenate these unseen samples together
                    ns.unseen_samples = np.concatenate( (ns.unseen_samples, newdata) ) 
        except:
            raise
        finally:
            sock.close()
    
    def __get_data_to_plot(self, ns):
        """
        @brief slice an amount of samples from the unseen_samples array to plot
        
        @param ns: the shared Namespace with attribute ns.unseen_samples
        """
        # shave the number of samples to plot
        x = ns.unseen_samples[:self.max_to_plot]
        
        # make the unseen samples array smaller 
        ns.unseen_samples = ns.unseen_samples[self.max_to_plot:]
         
        return x
       
    def __initialize_plot(self):
        """
        @brief initialize the figure to plot the timeseries and power spectrum
        of a predefined slice of the samples
        
        @return time_ax, fft_ax: the time and fft axes objects
        """
        # in interactive mode
        pl.ion() 
        fig = pl.figure()
        
        # make room for labels
        pl.subplots_adjust(hspace=0.3)
        
        # create and label the time axes
        time_ax = pl.subplot(2,1,1)
        
        # create and label the power axes
        fft_ax = pl.subplot(2,1,2)
        
        return time_ax, fft_ax
        
    def __plot_data(self, time_ax, fft_ax, data):
        """
        @brief plot the timeseries and power spectrum of data
        
        @param time_ax: the Axes object corresponding to timseries subplot
        @param fft_ax: the Axes object corresponding to power subplot
        @param data: the data to plot
        """
        
        # clear the axes to remove old data
        fft_ax.cla()
        time_ax.cla()
        
        # get the time array (in microseconds)
        ts = np.arange(0, self.dt*self.max_to_plot, self.dt)*1e6
        
        # plot the real and if data is DDC, the imaginary parts of timeseries
        time_ax.plot(ts, data.real, c='b')
        if self.dtype == 'ddc':
            time_ax.plot(ts, data.imag, c='r' )
             
        # compute the power spectrum of timeseries and plot
        freqs, power = digital_utils.power(data, timestep=self.dt)
        fft_ax.plot( freqs, power, c='k')
        
        # label the axes and set limits
        fft_ax.set_xlabel('frequency (Hz)', fontsize=16)
        fft_ax.set_ylabel('power', fontsize=16)
        
        time_ax.set_xlabel(r'time ($\mu$s)', fontsize=16)
        time_ax.set_ylabel('signal amplitude', fontsize=16)
        time_ax.set_xlim(0, self.dt*self.show*1e6)
        
        # draw and then we are finished
        pl.draw()
         
        return
         
    def continuous_plot(self, ns, trig):
        """
        @brief continuously plot a set number of samples from ns.unseen_samples
        
        @param ns: the shared Namespace between the two running Processes
        (multiprocessing.Manager.Namespace)
        @param trig: a trigger event to make sure we don't write/read shared array
        at same time (multiprocessing.Event)
        """
        
        # first, collect enough data to fill unseen_samples array
        while len(ns.unseen_samples) < self.max_to_plot:
            trig.clear() # will receive data when trig is clear
        
        # initialize two subplots for timeseries and FFT of signal
        time_ax, fft_ax = self.__initialize_plot()
            
        # plot continuously
        while True:
            
            # set the trigger to true while we slice the data to plot
            trig.set()
            data = self.__get_data_to_plot(ns)
            trig.clear()
            
            # plot the timeseries and FFT
            self.__plot_data(time_ax, fft_ax, data)    
            
       
if __name__ == '__main__':
    
    # parse the input arguments
    parser = argparse.ArgumentParser(description="receive signal data and plot continously")
    parser.add_argument('--dt', type=float, default=5e-9, help='timestep of data file')
    parser.add_argument('--dtype', type=str, default='ddc', choices=['ddc', 'data'], help='type of data being read')
    parser.add_argument('--port', type=int, default=12345, help='port number')

    args = parser.parse_args()
   
    # initialize the class and start receiving
    r = receiveUDP(timestep=args.dt, dtype=args.dtype, port=args.port)
    r.start()
