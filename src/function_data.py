import struct

def function(data1,data2,data3,data4):
                aa=data1
                aa=aa<<8|data2
                bb=data3
                bb=bb<<8|data4
                raw = struct.pack('>HH',aa,bb)
                data= struct.unpack('>f',raw)[0]
                return(data)

def function1(data1,data2):
                aa=data1
                aa=aa<<8|data2
                data=aa
                return(data)

def function2(data1,data2,data3,data4):
                aa=data1
                aa=aa<<8|data2
                bb=data3
                bb=bb<<8|data4
                if aa-32767>0: 
                        #print("aa signed")
                        data= (aa-65536)*65536 + (bb-0)
                else:
                        #print("aa and bb unsigned")
                        data= (aa-0)*65536 + (bb-0)
                return(data)

def function3(data1,data2,data3,data4):
                aa=data1
                aa=aa<<8|data2
                bb=data3
                bb=bb<<8|data4
                if aa-32767>0 and bb-32767>0:
                        #print("aa and bb signed")
                        data= (aa-65536)*10000 + (bb-65536)
                else:
                        #print("aa and bb unsigned")
                        data= (aa-0)*10000 + (bb-0)
                return(data)

def function4(data1,data2,data3,data4,data5,data6,data7,data8):
                aa=data1
                aa=aa<<8|data2
                bb=data3
                bb=bb<<8|data4
                cc=data5
                cc=cc<<8|data6
                dd=data7
                dd=dd<<8|data8
                aaaa=aa<<16|bb
                bbbb=cc<<16|dd
                c=aaaa<<32|bbbb
                data=struct.unpack('d', struct.pack('Q', c))[0]
                return(data)
