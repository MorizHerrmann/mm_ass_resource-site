# SECTIONALIZE DATA - MICROMETEOROLOGY | ASSIGNMENT 4 | WIND RESOURCE AND SITE ASSESSMENT ##############################

"""
Environment for the whole exercise. Contains constants and methods which are based on those.
"""

# IMPORTS ##############################################################################################################

from toolkit import *
import scipy.optimize as opt

# ENVIRONMENT ##########################################################################################################


class Environment:
    def __init__(self):
        """
        load constants
        """
        # roughness lengthes
        self.z0_water = 0.02e-2     # [m] roughness length over water
        self.z0_land = 3e-2         # [m] roughness length over lande
        self.z_hub = 110            # [m] hub height
        self.z_mast = 70            # [m] mast height

        # sites
        self.sites = ['nyborg', 'korsor']
        self.z0_nyb = np.array([*[self.z0_water] * 6, *[self.z0_land] * 6])
        self.z0_kor = np.array([*[self.z0_land] * 6, *[self.z0_water] * 6])
        self.z0_sites = [self.z0_nyb, self.z0_kor]

        # operation constants
        self.T = 365.25 * 24    # [hours]
        self.u_rated = 12.5     # [m/s] rated wind speed
        self.u_cutout = 25      # [m/s] cut out wind speed
        self.p_rated = 6e6      # [W] rated power

        # else constants
        self.karman = 0.4
        self.A = 1.8                                        # GDL
        self.B = 4.5                                        # GDL
        self.fc = 2 * 7.2921e-5 * np.sin(55 * np.pi / 180)  # coriolis factor

    def P(self, u):
        """
        evaluate power curve
        :param u: wind speed (np.ndarray)
        :return: power (np.ndarray)
        """
        # masks
        subrated = u < self.u_rated
        rated = (self.u_rated < u) & (u < self.u_cutout)
        overrated = u > self.u_cutout

        p = np.zeros(u.shape)

        p[subrated] = self.p_rated * np.power(u[subrated] / self.u_rated, 3)
        p[rated] = self.p_rated * np.ones(u[rated].shape)
        p[overrated] = np.zeros(u[overrated].shape)

        return p

    def AEP(self, a, k, f):
        """

        :param a: weibull scale parameter
        :param k: weibull shape parameter
        :param f: frequency of occurrence
        :return: total annual energy production of all sections
        """

        # calculate AEP for each section
        aep_sec = np.zeros(a.shape)
        u = np.linspace(0, self.u_cutout, 100)
        for m in range(len(aep_sec)):
            aep_sec[m] = self.T * f[m] * np.trapz(np.multiply(weibull_pdf(u, a[m], k[m]), self.P(u)), u)

        print(aep_sec)
        # sum it up
        return np.sum(aep_sec)

    def extrapolate2sites(self, input_file, output_dir):
        """
        i think this is obsolete, because it extrapolates each event independently
        :param input_file: file name
        :param output_dir: path where the result is saved
        :return: (save extrapolated wind speed)
        """

        # load data
        data = np.loadtxt(input_file)
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

            # loop over each time step
            u_site = np.zeros(u.shape)
            for t in range(T):
                if t % 5000 == 0: print(f'{t/T*100.:1f}%')
                def spec_GDL(uf): return self.GDL(G[t], uf, z0[t])
                uf_site = opt.fsolve(spec_GDL, uf_sprog[t])[0]
                u_site[t] = np.multiply(uf_site / self.karman, np.log(self.z_hub / z0[t]))

            # save extrapolated data
            data_expol = data
            data_expol[:, 5] = u_site

            np.savetxt(output_dir + site + '.csv', data_expol)

    def GDL(self, G, uf, z0):
        """
        implicit GDL function
        :param G: geostrophic wind
        :param uf: friction velocity
        :param z0: roughness length
        :return: loss
        """
        return G - np.multiply(uf / self.karman, np.sqrt(np.power(np.log(np.divide(uf, z0) / self.fc) - self.A, 2) + self.B ** 2))

    def geostrophic_wind(self, a, k):
        """
        :param a: weibull scale parameter
        :param k: weibull shape parameter
        :return: geostrophic wind, friction velocity
        """

        # calculate mean wind speed from weibull distribution
        u = np.multiply(a, gamma(1 + 1 / k))

        # calculate friction velocity
        uf = u * self.karman / (np.log(self.z_mast / self.z0_water))

        # calculate geostrophic wind
        G = uf / self.karman * np.sqrt((np.log(uf / (self.z0_water * self.fc)) - self.A) ** 2 + self.B ** 2)

        return G, uf

    def extrapolate_mean(self, akf_file, output_file):
        """
        extrapolate weibull parameters
        :param akf_file: file with scale parameter A, shape parameter k and frequency of occurrence f
        :param output_file: path/name of output file
        :return: (save extrapolated weibull parameters -> akf-file)
        """
        # load weibull for each section
        a, k, f = load_akf(akf_file)

        # compute mean, friction velocity and geostrophic wind
        G, uf_sprogo = self.geostrophic_wind(a, k)

        # re-calculate mean wind at site
        for s, site in enumerate(self.sites):
            print(site)
            # compute the roughness length for each wind
            z0 = self.z0_sites[s]


            uf_site = np.ndarray(uf_sprogo.shape)
            for sec in range(12):
                def spec_GDL(uf): return self.GDL(G[sec], uf, z0[sec])
                uf_site[sec] = opt.fsolve(spec_GDL, uf_sprogo[sec])[0]

            u_site = np.multiply(uf_site / self.karman, np.log(self.z_hub / z0))
            print(f'Mean wind: {u_site}')

            # calculate weibull at site
            k_site = k
            a_site = np.divide(u_site, gamma(1 + 1 / k))
            f_site = f

            labels = ['A', 'k', 'f']
            data = np.array([a_site, k_site, f_site]).transpose()

            df = pd.DataFrame(data, columns=labels)

            df.to_csv(output_file)
