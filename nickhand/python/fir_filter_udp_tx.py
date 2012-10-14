# 
#  fir_filter_udp_tx.py
#  <classes to transmit data to a client from ROACH via UDP>
#  
#  Created by Nick Hand on 2012-10-12.
# 
import socket, time, struct
import optparse, sys, digital_utils

class ROACHInterface(object):
    """
    @brief a class containing methods to interface with ROACH 
    """
    
    def __init__(self, pid):
       """
       @brief initialize the class
       @param pid: the process ID corresponding to the 
       running BOF file on the ROACH (int)
       """ 
        
       self.path      = "/Users/Nick/proc/%d/hw/ioreg/" %pid
       self.data_bram = self.path + 'data_bram'
       self.ddc_bram  = self.path + 'ddc_bram'
       self.ddc_addr  = self.path + 'ddc_addr'
       self.lo_path   = self.path + 'freq' 
       self.trig_path = self.path + 'trig'
     
     
    def set_lof(self, f_MHz, clk_MHz=200., freq_bits=10):
        """
        @brief set the local oscillator frequency (LOF), which
        is written as an unsigned 4 byte int in self.lo_path
        
        @param f_MHz: the desired LOF to set in MHz (float)
        @param clk_MHZ: the clock frequency of the ROACH in MHz (float)
        @param freq_bit: number of bits in the frequency period is 2**freq_bits (int)
        """
        
        # compute the int corresponding to desired LOF
        lof_int = digital_utils.compute_lof_int(f_MHz, clk_MHz, freq_bits)
        f = open(self.lo_path, 'w')
        f.write(struct.pack('>I', val))
        f.close()  

    def trig_data_bram(self):
        """
        @brief trigger the data_bram file so output is written
        """

        f = open(self.trig_path, 'w')
        f.write("\x00\x00\x00\x01")
        f.seek(0)
        
        f.write("\x00\x00\x00\x00")
        f.close()

    def read_data_bram(self):
        """
        @brief read the data from the data_bram file
        """
        f = open(self.data_bram)
        data = f.read()
        f.close()

        return data

  
class transmitUDP(object):
    """
    @brief a class to read data from the ROACH and transmit
    to a client via User Datagram Protocol (UDP)
    """
    
    def __init__(self, pid, host='192.168.1.101', port=12345):
        """
        @brief initialize the class, given a process ID, host and port
        
        @param pid: the process ID of the running BOF file (int)
        @param host: the IP address of the client to transmit to (str)
        @param port: the port over which to communicate (int)
        """
        
        self.ri = ROACHInterface(pid)
        self.host = host
        self.port = port
           
    def send_data_bram(self):
        """
        @brief transmit continuously the data from the data_bram file
        
        @param continuous: whether to continually send the contents 
        of the file (bool)
        """
        # open the socket and connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect((self.host, self.port))
        
        # make sure we always close the socket if something crashes
        try: 
            # bytes per packet to send, since all of data_bram is too much for one packet
            packetSize=4096 
            
            # read and send data continuously
            while True:
                    
                # trigger the data bram
                self.ri.trig_data_bram()
            
                # wait 10 ms for data to fill up (is this needed?)
                time.sleep(1e-2)
            
                # read the data bram file
                output = self.ri.read_data_bram()
            
                # send the data in packets of size packetSize
                lo = 0
                while lo < len(output):
                    
                    hi = min(lo+packetSize, len(output))
                      
                    # sleep for 10 ms so we don't send data too fast
                    time.sleep(1e-2) 
                        
                    # send the data packet
                    sock.send(output[lo:hi])
                        
                    lo += packetSize
        except:
            raise
        finally:
            sock.close()
            
        return
        
    def send_ddc_bram(self, wordlength=4):
        """
        @brief transmit continously the data from the ddc_bram file
        
        @param wordlength: bytes per value (int)
        """
        # open the ddc data/address files
        f_data = open(self.ri.ddc_bram)
        f_addr = open(self.ri.ddc_addr)
        
        # always make sure we close files and socket
        try:
            
            # open the socket and connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect((self.host, self.port))
            
            old_addr = 0
            # send data packets continuously
            while True:
            
                # read in the current ddc address and then seek back to the beginning           
                new_addr = f_addr.read()
                f_addr.seek(0)
                
                # unpack the new address, which is a 4 byte unsigned int
                new_addr = struct.unpack('>i', new_addr)[0]
                
                # check if there is overfill back to address 0
                if new_addr > old_addr:
                    
                    bytesToRead = wordlength*(new_addr - old_addr)
                    output = f_data.read(bytesToRead)
                    
                else:
                    
                    # read the rest of the file
                    # assuming placeholder at old_addr
                    data_end = f_data.read()
                    
                    # read the beginning data up to new_addr
                    f_data.seek(0)
                    data_begin = f_data.read(wordlength*new_addr)
                    
                    # concatenate the two data outputs
                    output = "".join([data_end, data_begin])
                
                # set old address to new address
                old_addr = new_addr
                
                # send the ouput packet
                sock.send(output)
        except:
            raise
        
        finally:
            f_data.close() 
            f_addr.close()
            sock.close()


if __name__ == '__main__':
    
    # parse using optparse b/c ROACH is not running 2.7
    o = optparse.OptionParser()
    o.add_option('-p', '--port', dest='port', type='int', default=12345, help='port number')
    o.add_option('-q', '--host', type='str', dest='host',default='192.168.1.100', help='ip address')
    o.add_option('-i', '--input', dest='get_input', action='store_true', default=False, help='transmit input signal')
    o.add_option('-w', '--wordlength', dest='wordlength', type='int', default=4, help='bytes per value')

    opts,args = o.parse_args(sys.argv[1:])
    
    # initialize the transmitUDP class
    t = transmitUDP(int(args[0]), host=opts.host, port=opts.port)
    
    # transmit input signal or DDC signal depending on optional arguments
    if opts.get_input:
        t.send_data_bram()
    else:
        t.send_ddc_bram()
