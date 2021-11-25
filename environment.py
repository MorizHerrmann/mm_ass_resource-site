import numpy as np
from scipy.special import gamma
from toolkit import *
import scipy.optimize as opt


class Environment:
    def __init__(self):
        self.z0_water = 0.02e-2     # [m] roughness length over water
        self.z0_land = 3e-2         # [m] roughness length over lande
        self.z_hub = 110            # [m] hub height
        self.z_mast = 70            # [m] mast height

        self.T = 365.25 * 24    # [hours]
        self.u_rated = 12.5     # [m/s] rated wind speed
        self.u_cutout = 25      # [m/s] cut out wind speed
        self.p_rated = 6e6      # [W] rated power

        self.karman = 0.4
        self.A = 1.8                                        # GDL
        self.B = 4.5                                        # GDL
        self.fc = 2 * 7.2921e-5 * np.sin(55 * np.pi / 180)  # coriolis factor

        # sites
        self.sites = ['nyborg', 'korsor']
        self.z0_nyb = np.array([*[self.z0_water] * 6, *[self.z0_land] * 6])
        self.z0_kor = np.array([*[self.z0_land] * 6, *[self.z0_water] * 6])
        self.z0_sites = [self.z0_nyb, self.z0_kor]

    def P(self, u):
        subrated = u < self.u_rated
        rated = (self.u_rated < u) & (u < self.u_cutout)
        overrated = u > self.u_cutout

        p = np.zeros(u.shape)

        p[subrated] = self.p_rated * np.power(u[subrated] / self.u_rated, 3)
        p[rated] = self.p_rated * np.ones(u[rated].shape)
        p[overrated] = np.zeros(u[overrated].shape)

        return p

    def AEP(self, wb_A, wb_k, f):
        """find the annual energy production from weibull parameters for all sections"""
        aep_sec = np.zeros(wb_A.shape)
        u = np.linspace(0, self.u_cutout, 100)
        for m in range(len(aep_sec)):
            aep_sec[m] = self.T * f[m] * np.trapz(np.multiply(weibull_pdf(u, wb_A[m], wb_k[m]), self.P(u)), u)
        return np.sum(aep_sec)

    def geostrophic_wind2(self, u):
        """
        calculate geostrophic wind at sprogo from wind speed
        :param u: wind speed
        :return: friction velocity
        """
        uf = u * self.karman / (np.log(self.z_mast / self.z0_water))
        G = uf / self.karman * np.sqrt((np.log(uf / (self.z0_water * self.fc)) - self.A) ** 2 + self.B ** 2)
        return G, uf

    def geostrophic_wind(self, wb_A, wb_k):
        """caclulate geostrophic wind at Sprogo from weibull distribution"""
        u = np.multiply(wb_A, gamma(1 + 1 / wb_k))
        uf = u * self.karman / (np.log(self.z_mast / self.z0_water))
        G = uf / self.karman * np.sqrt((np.log(uf / (self.z0_water * self.fc)) - self.A) ** 2 + self.B ** 2)

        return G, uf

    def extrapolate2sites(self, file):
        """
        add geostrophic wind to data
        :param file: file name
        :return:
        """

        # load data
        data = np.loadtxt(file)
        T = len(data)
        u = data[:, 5]
        easterly = data[:, 6] <= 180
        westerly = data[:, 6] > 180

        # calculate geostrophic wind
        uf_sprog = u * self.karman / (np.log(self.z_mast / self.z0_water))
        G = uf_sprog / self.karman * np.sqrt((np.log(uf_sprog / (self.z0_water * self.fc)) - self.A) ** 2 + self.B ** 2)

        for s, site in enumerate(self.sites):

            # compute the roughness length for each wind
            z0 = np.zeros(u.shape)
            if site == 'nyborg':
                z0[easterly] = self.z0_water * np.ones(z0[easterly].shape)
                z0[westerly] = self.z0_land * np.ones(z0[westerly].shape)
            elif site == 'korsor':
                z0[westerly] = self.z0_water * np.ones(z0[westerly].shape)
                z0[easterly] = self.z0_land * np.ones(z0[easterly].shape)

            u_site = np.zeros(u.shape)
            for t in range(T):
                if t % 5000 == 0: print(f'{t/T*100.:1f}%')
                def spec_GDL(uf): return self.GDL(G[t], uf, z0[t])
                uf_site = opt.fsolve(spec_GDL, uf_sprog[t])[0]
                u_site[t] = np.multiply(uf_site / self.karman, np.log(self.z_hub / z0[t]))

            # save extrapolated data
            data_expol = data
            data_expol[:, 5] = u_site

            np.savetxt(site + '_' + file, data_expol)

    def GDL(self, G, uf, z0):
        """implicit GDL function"""
        root = np.sqrt(np.power(np.log(np.divide(uf, z0) / self.fc) - self.A, 2) + self.B ** 2)
        out = G - np.multiply(uf / self.karman, root)
        return out
