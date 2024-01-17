#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/alfredo/Desktop/PhD/LhARA/LhARAlinearOptics/01-Code/')

import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import Particle as Prtcl

import BeamLine as BL

'''
Things to revise:
    
    Arbitrary parameters for centering structures in plt_apt (5E-3, 6E-3)
    Automatize elliptical aperture

Methods to do list:
    Particle number along beamline
    Phase space evolution along beamline
    Twiss parameters along beamline and brightness (in development as sequential code)
    
'''


#------------Module methods:---------------------------------

def find_rows(dataframe, target_name, avoid = None, use_include = False, include = None):

    if 'Element' in dataframe.columns:
        if use_include == True:
            matching_rows = dataframe.index[dataframe['Element'].str.contains(target_name, case=False) &\
                                            (dataframe['Comment'].astype(str).str.strip() != avoid) &\
                                            (dataframe['Parameter'].astype(str).str.strip() == include)
                                            ].tolist()
        else:
            matching_rows = dataframe.index[dataframe['Element'].str.contains(target_name, case=False) &\
                                            (dataframe['Comment'].astype(str).str.strip() != avoid)
                                            ].tolist()            
            
        if len(matching_rows) != 0:
            return matching_rows
        
        else:
            print(f"No matching rows for '{target_name}' found in the 'Element' column.")
            return pd.DataFrame()  
        
    else:
        print("DataFrame does not have an 'Element' column.")
        return pd.DataFrame()

fig, axs = plt.subplots(3, 1, figsize=(11, 11))

#-------------------Class definition----------------------------


class BeamlinePlotter(object):
    
    import numpy as np
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import Particle as Prtcl

    __Debug     = False
    __instance  = None
    __Facility = None 
    
#-------"Get" Methods-------------------- 
    
    def get_zlist(HOMEPATH = os.getenv('HOMEPATH'), filename = None):
        
        aux = 0
        z = []
        params  = pd.read_csv(HOMEPATH + '/11-Parameters/' + filename)
        indexes = params[params['Parameter'] == 'Length'].index.tolist()
        for i in indexes:
            aux += float(params['Value'][i])
            z.append(aux)
        
        z.insert(0, 0.) #insert source position
            
        return z
    
    def get_elementlist(HOMEPATH = os.getenv('HOMEPATH'), filename = None):
        
        params = pd.read_csv(HOMEPATH + '/11-Parameters/' + filename)
        my_list = []
        prev_element = None

        for element in params['Element']:
            if element != prev_element:
                my_list.append(element)
            prev_element = element
            
        #Eliminate the Aperture occurences before and after every solenoid
        new_list = []
        i = 0
        while i < len(my_list):
            if my_list[i] == 'Solenoid' and i > 0 and i < len(my_list) - 1 and my_list[i - 1] == 'Aperture' and my_list[i + 1] == 'Aperture':
                new_list.append(my_list[i])
                new_list.append('Solenoid_end')
                i += 2  # Skip the 'Apt' elements
            elif my_list[i] == 'Aperture' and i > 0 and i < len(my_list) - 1 and my_list[i + 1] == 'Solenoid':
                i += 1  # Skip the 'Apt' elements
            else:
                new_list.append(my_list[i])
                i += 1
        my_list = new_list
        
        #Eliminate one of the apertures for every Fquad and Dquad
        
        lst = my_list
        result = []
        skip_next = False

        for i in range(len(lst)):
            if skip_next:
                skip_next = False
                #continue

            if lst[i] == "Aperture" and i + 1 < len(lst) and (lst[i + 1] == "Fquad" or lst[i + 1] == "Dquad"):
                skip_next = True
            else:
                result.append(lst[i])
        my_list = result
        
        #Eliminate the Drifts
        new_list = []
        for i in my_list:
            if i != 'Drift' and i != 'Global':
                new_list.append(i)
        
        return new_list
    
    def get_ReferenceEnergy(HOMEPATH = os.getenv('HOMEPATH'), filename = None):
        params = pd.read_csv(HOMEPATH + '/11-Parameters/' + filename)
        index  = params[params['Parameter'] == 'Kinetic energy'].index
        E      = float(params['Value'][index])
        return E
    
#--------Beamline plotting Methods---------------    
    
    def Tracer(mini, maxi, filename, maxz = 2.135, facility = None, HOMEPATH = os.getenv('HOMEPATH'), label = None, NEvts = False, alpha = 0.5, colour = 'r'):
          
                ParticleFILE = Prtcl.Particle.openParticleFile(HOMEPATH + "/99-Scratch", filename)
        
                EndOfFile = False
                iEvt      = 0
                iPrtcl    = None
                
                DRACObI  = BL.BeamLine(HOMEPATH + '/11-Parameters/' + facility)
                
                RefE = BeamlinePlotter.get_ReferenceEnergy(HOMEPATH=HOMEPATH, filename = facility)
                
                try:
                    
                        while not EndOfFile:
                                
                                EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
        
                                iPrtcl = Prtcl.Particle.getParticleInstances()[1] #used to be 0 in the previous PhaseSpace implementation
                    
                                if iPrtcl.getz()[-1] > maxz: #the ones that get to the end of beamline
                    
                                            if mini < iPrtcl.getTraceSpace()[0][5] + RefE < maxi:
                                                    
                                                    iEvt += 1
                                                    particle = iPrtcl
                                                
                                                    x = []
                                                    y = []
                                                    z = particle.getz()
                                                    
                                            
                                                    for i in range(len(particle.getTraceSpace())):
                                                          x.append(particle.getTraceSpace()[i][0])
                                                          y.append(particle.getTraceSpace()[i][2])
                                                          
                                                    xd = x[-1]
                                                    yd = y[-1] 
                                                          
                                                    if iEvt == 1:      
                                                        axs[0].plot(xd, yd, 'o', color = colour, alpha = alpha, label = label)
                                                    
                                                    else:
                                                        axs[0].plot(xd, yd, 'o', color = colour, alpha = alpha)
                                                    axs[1].plot(z, x, color = colour, alpha = alpha)
                                                    axs[2].plot(z, y, color = colour, alpha = alpha)
                                            
                                                    cleaned = Prtcl.Particle.cleanParticles()
                                                    
                                                    if iEvt == NEvts: #Ends the loop if everything is plotted
                                                        EndOfFile = True    
                                            else:
                                                cleaned = Prtcl.Particle.cleanParticles()
                                else:
                                                                       
                                    cleaned = Prtcl.Particle.cleanParticles()

                except: #Handles the exception if you already plotted all the particles within energy range
                            IndexError
                            print('All particles within energy range E =', str(label) ,'have been plotted')
                            pass


    def plt_apt(filename, HOMEPATH = os.getenv('HOMEPATH')): #automatize the position of the apertures in the beamline

            params = pd.read_csv(HOMEPATH + '/11-Parameters/' + filename)
            j      = find_rows(params, 'Aperture', avoid='Radius of solenoid bore')

            z        = BeamlinePlotter.get_zlist(HOMEPATH  = HOMEPATH, filename = filename)
            #print(z, len(z))
            elements = BeamlinePlotter.get_elementlist(HOMEPATH  = HOMEPATH, filename = filename)
            #print(elements, len(elements))
            aux_elem = elements.copy()
            
            index = []
            
            while aux_elem.count('Aperture') != 0:
                ind = aux_elem.index('Aperture')
                index.append(ind)
                aux_elem.remove('Aperture')
                aux_elem.insert(ind, 'removed')
            
            #print(index)
            
            for i in range(len(index)):

                label = 'Aperture'

                apt_posi = z[index[i]]

                apt_rad = float(params.iloc[j[i]][5])

                apt_z = np.full(5, apt_posi)

                apt_x = np.array([-3*apt_rad, -apt_rad, None, apt_rad, 3*apt_rad]) 

                axs[1].plot(apt_z, apt_x, linestyle='-', label = 'Aperture %d'%(i+1))
            

              #  if index[i] == 2: #Automatizar apertura elíptica
               #         apt_rad = params.iloc[9][5] # for eliptical aperture, new radius in y-plane
                apt_y = np.array([-3*apt_rad, -apt_rad, None, apt_rad, 3*apt_rad])
                axs[2].plot(apt_z, apt_y, linestyle='-', label = label)
                
            print('Aperture plot complete')


    def plt_quad(filename, HOMEPATH = os.getenv('HOMEPATH')):

            filedir    = os.path.join(HOMEPATH, \
                             '11-Parameters/' + filename)
            params = pd.read_csv(filedir)
            z = BeamlinePlotter.get_zlist(HOMEPATH  = HOMEPATH, filename = filename)
            #print(z)
            elements = BeamlinePlotter.get_elementlist(HOMEPATH  = HOMEPATH, filename = filename)
            #print(elements)
            Daux_elem = elements.copy()
            Faux_elem = elements.copy()
            
            Dindex = []
            Findex = []
            
            while Daux_elem.count('Dquad') != 0:
                ind = Daux_elem.index('Dquad')
                Dindex.append(ind)
                Daux_elem.remove('Dquad')
                Daux_elem.insert(ind, 'removed')
            
            while Faux_elem.count('Fquad') != 0:
                ind = Faux_elem.index('Fquad')
                Findex.append(ind)
                Faux_elem.remove('Fquad')
                Faux_elem.insert(ind, 'removed')
                
            j      = find_rows(params, 'Dquad', use_include = True, include = 'Length') #esto incluye la fila con strength
            for i in range(len(j)): #formerly j
                    label_name = 'DQuad'

                    quad_lnth = float(params.iloc[j[i]][5])
                    quad_posi = z[Dindex[i]]+quad_lnth
                    
                    ori = -1

                    quad_coords = [(quad_posi - quad_lnth, ori*6E-3), (quad_posi -(quad_lnth), ori*5E-3), (quad_posi, ori*5E-3), (quad_posi, ori*6E-3), (quad_posi - quad_lnth, ori*6E-3)]      
                    quad_w, quad_h = zip(*quad_coords)

                    axs[1].plot(quad_w, quad_h, linestyle='-', label = label_name)
                    axs[2].plot(quad_w, quad_h, linestyle='-', label = label_name)
                    
            j      = find_rows(params, 'Fquad', use_include = True, include = 'Length')
            
            for i in range(len(j)):
                    label_name = 'FQuad'

                    quad_lnth = float(params.iloc[j[i]][5]) #formerly 5
                    quad_posi = z[Findex[i]]+quad_lnth
                    print(quad_lnth)

                    ori = 1

                    quad_coords = [(quad_posi - quad_lnth, ori*6E-3), (quad_posi -(quad_lnth), ori*5E-3), (quad_posi, ori*5E-3), (quad_posi, ori*6E-3), (quad_posi - quad_lnth, ori*6E-3)]      
                    quad_w, quad_h = zip(*quad_coords)

                    axs[1].plot(quad_w, quad_h, linestyle='-', label = label_name)
                    axs[2].plot(quad_w, quad_h, linestyle='-', label = label_name)
                    
            print('Quadrupole plot complete')
            

    def plt_solenoid(filename, HOMEPATH = os.getenv('HOMEPATH')):
                
            params = pd.read_csv(HOMEPATH + '/11-Parameters/' + filename)
            j      = find_rows(params, 'Solenoid', use_include = True, include = 'Length')
            z = BeamlinePlotter.get_zlist(HOMEPATH  = HOMEPATH, filename = filename) 
            elements = BeamlinePlotter.get_elementlist(HOMEPATH = HOMEPATH, filename = filename)
            aux_elem = elements.copy()
            
            index = []
            
            while aux_elem.count('Solenoid') != 0:
                ind = aux_elem.index('Solenoid')
                index.append(ind)
                aux_elem.remove('Solenoid')
                aux_elem.insert(ind, 'removed')
            
            for i in range(len(j)):

                    sole_posi = z[index[i]]
                    sole_rad  = float(params.iloc[j[i]-1][5])
                    sole_lnth = float(params.iloc[j[i]][5])

                    sole_coords = [(sole_posi - sole_lnth, sole_rad), (sole_posi -(sole_lnth), -sole_rad), (sole_posi, -sole_rad), (sole_posi, sole_rad), (sole_posi - sole_lnth, sole_rad)]  
      
                    sole_w, sole_h = zip(*sole_coords)

                    axs[1].plot(sole_w, sole_h, linestyle='-', label = 'S%d'%(i+1))
                    axs[2].plot(sole_w, sole_h, linestyle='-', label = 'S%d'%(i+1))
                    
            print('Solenoid plot complete')
            

    def plt_save(path = '99-Scratch/ParticleTrajectory.pdf'):

            axs[0].grid(True)
            axs[0].legend(loc = 'upper left', fontsize = 'small')
            axs[0].set_xlabel('x-axis')
            axs[0].set_ylabel('y-axis')
            axs[0].set_title('Particle Beam after Final Collimator x-y plane')

            axs[1].grid(True)
            axs[1].legend(loc = 'upper left', bbox_to_anchor=(-0.2, 0.5, 0.5, 0.5), fontsize = 'small')
            axs[1].set_xlabel('z-axis')
            axs[1].set_ylabel('x-axis')
            axs[1].set_title('Particle Trajectory x-z plane')

            axs[2].grid(True)
            axs[2].legend(loc = 'upper left', bbox_to_anchor=(-0.2, 0.5, 0.5, 0.5), fontsize = 'small')
            axs[2].set_xlabel('z-axis')
            axs[2].set_ylabel('y-axis')
            axs[2].set_title('Particle Trajectory y-z plane')

            fig.tight_layout()
            plt.savefig(path)
            plt.close()


    def plt_show():

            axs[0].grid(True)
            axs[0].legend(loc = 'upper left', fontsize = 'small')
            axs[0].set_xlabel('x-axis')
            axs[0].set_ylabel('y-axis')
            axs[0].set_title('Particle Beam at Final Collimator x-y plane')

            axs[1].grid(True)
           # axs[1].legend(loc = 'upper left', fontsize = 'small')
            axs[1].set_xlabel('z-axis')
            axs[1].set_ylabel('x-axis')
            axs[1].set_title('Particle Trajectory x-z plane')

            axs[2].grid(True)
          #  axs[2].legend(loc = 'upper left', fontsize = 'small')
            axs[2].set_xlabel('z-axis')
            axs[2].set_ylabel('y-axis')
            axs[2].set_title('Particle Trajectory y-z plane')

            fig.tight_layout()
            plt.show()
            
            
    def plt_prtclnumberAFR(fig, axs ,Nevts = 5000, data_file = None, parameter_file = None, HOMEPATH = os.getenv('HOMEPATH')):

            '''
            Work in progress
            '''
            #ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "DRACOsimuLsrDrvn.dat")
            ParticleFILE = Prtcl.Particle.openParticleFile(HOMEPATH + "/99-Scratch", data_file)
            EndOfFile = False
            iPrtcl    = None
            n_den = np.array([])

            z = BeamlinePlotter.get_zlist(HOMEPATH = HOMEPATH, filename = parameter_file)        

            for i in range(len(z)): #number of co-ordinates to read per particle
                    Evt = 0
                    count = 0

                    #ParticleFILE = Prtcl.Particle.openParticleFile("99-Scratch", "DRACOsimuLsrDrvn.dat")
                    ParticleFILE = Prtcl.Particle.openParticleFile(HOMEPATH + "/99-Scratch", "DRACOsimuLsrDrvn.dat")
                    
                    try:
                    
                        while not EndOfFile:
                            
                                EndOfFile = Prtcl.Particle.readParticle(ParticleFILE)
                                iPrtcl    = Prtcl.Particle.getParticleInstances()[0]
                                Evt += 1

                                while iPrtcl.getz()[len(iPrtcl.getz())-1] >= z[i]:
                                        count += 1
                                        break
                    
                    except:
                        IndexError
                        print('Counted successfully at position:', z[i],'Count:', (count))
                        pass

                    cleaned = Prtcl.Particle.cleanParticles()

                    n_den = np.append(n_den, count)
                    #print('Position:', z[i] ,'Count:', (count))
                    
                    partic_left = count/Nevts #add particular ase in which we go through all the particles  
                    
                    print(partic_left)


            axs.plot(z[0:10], n_den[0:10], label = 'Transmission efficiency: %.3f'% partic_left)
            axs.grid(True)
            axs.set_title('Particle Number across Beamline - Air Section')
            axs.legend(loc = 'best')
            fig.tight_layout()
            #plt.savefig('99-Scratch/NumberDensity.pdf')
            plt.show()
            #plt.close()
            

#%% Method for plotting a colimator, not in use for now


def plt_colim(z): 
        HOMEPATH = os.getenv('HOMEPATH')        
        filename    = os.path.join(HOMEPATH, filename)
        params = pd.read_csv(filename)
        
        elip = False #figure out how to automatise this
        
        j = 24#location of aperture in parameters file

        col_posi = z #added a false drift afteer colimator so we can evaluate which ones get to the target
        col_rad = params.iloc[j][5]
            
        print(col_posi)
        print(col_rad)
            
        col_z = np.full(5, col_posi)
        col_x = np.array([-3*col_rad, -col_rad, None, col_rad, 3*col_rad]) #6E-3 set arbitrarily

        axs[1].plot(col_z, col_x, linestyle='-', label = 'Colimator')

        if elip == True:
            col_rad = params.iloc[9][5] # for eliptical aperture, new radius in y-plane
            
        col_y = np.array([-3*col_rad, -col_rad, None, col_rad, 3*col_rad])

        axs[2].plot(col_z, col_y, linestyle='-', label = 'Colimator')
