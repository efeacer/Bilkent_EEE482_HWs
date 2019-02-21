'''
Code for EEE482 homework 1, 2019 Spring. 
Author: Efe Acer
'''

import sys

question = sys.argv[1]

def efe_acer_21602217_hw1(question):
    if question == '1' :
        print(1)
        ##question 1 code goes here
        
    elif question == '2' :
        
        # Necassary imports
        import numpy as np 
        import matplotlib.pyplot as plt
        from scipy.io import loadmat # to be able to use .mat file in the python environment

        # QUESTION 2
        print('QUESTION 2\n')

        data = loadmat('XData.mat')
        x_data = data['x'].flatten()
        print('The dataset: ', x_data, '\n')

        # PART A
        print('PART A\n')

        mean = np.mean(x_data)
        median = np.median(x_data)
        print('Sample mean: %f \nSample median: %f\n' % (mean, median))

        # PART B
        print('PART B\n')

        std = np.std(x_data)
        q25, q75 = np.percentile(x_data, [25, 75])
        iqr = q75 - q25
        print('Sample standard deviation: %f \nSample inter-quartile range: %f\n' %
              (std, iqr))

        figure_num = 1 # to keep track of a figure's number 

        # PART C
        print('PART C\n')

        x_range = [70, 130]
        num_bins = [3, 6, 12]
        colors = ['g', 'r', 'b']

        print('The histograms:')
        for i in range(3):
            plt.figure(figure_num)
            figure_num += 1
            plt.title('Histogram of the aggregated responses')
            plt.ylabel('Counts')
            plt.xlabel('Aggregated responses')
            plt.hist(x_data.flatten(), bins=num_bins[i], range=x_range, 
                              color=colors[i], edgecolor='black', linewidth=1.2)
            plt.show(block=False)

        # PART D
        print('PART D\n')

        plt.figure(figure_num)
        figure_num += 1

        # Python equivalent of the Matlab Normal Quantile Plot code given in the assignment
        y = np.sort(x_data)
        n = np.size(x_data)
        f = (np.arange(1, n + 1) - 3/ 8) / (n + 1 / 4)
        q = 4.91 * (f ** 0.14 - (1 - f) ** 0.14)
        plt.grid()
        plt.plot(q, y, '*-')

        print('The Normal Quantile Plot of the dataset:')
        plt.show(block=False)
        print('In a Normal Quantile Plot, a roughly straight line is formed ' + 
              'when both sets of quantiles came from the same Normal ' + 
              'Distribution. Thus, samples of X are normally distributed.\n')

        # PART E
        print('PART E\n')

        # Function to perform bootstrap resampling
        def bootstrap_resampling(data, bootstraps, stat_func):
            """
            Given the data, number of bootstrapping iterations and the statistic of 
            interest; this function returns a list of statistics obtained from each 
            bootstrapped sample of the original data.
            Args:
                data: The original data
                bootstraps: The number of bootstrapping iterations
                stat_func: The function to compute the statistic of interest 
                    (e.g.: np.mean, np.std, etc.)
            Returns: 
                bootstrap_replicate: The mean of all bootstrap replicates
                standard_error: The standard error of the bootstrap replicate
                bootstrap_replicates: The list of statistics obtained from the 
                    bootstrapped samples
            """
            bootstrap_replicates = []
            sample_size = np.size(data)
            for _ in range(bootstraps):
                bootstrap_sample = np.random.choice(data, sample_size, replace=True)
                bootstrap_replicates.append(stat_func(bootstrap_sample))
            return np.mean(bootstrap_replicates), np.std(bootstrap_replicates), bootstrap_replicates

        # Function to compute the confidence interval of data samples
        def compute_confidence_interval(data, confidence):
            """
            Given the data and the confidence level, computes the confidence interval
            of the data samples.
            Args:
                data: The given data
                confidence: The confidence level, known as alpha (between 0 and 100)
            Returns:
                lower: The lowerbound of the confidence interval
                upper: The upperbound of the confidence interval
            """
            sorted_data = np.sort(data)
            lower = np.percentile(sorted_data, (100 - confidence) / 2)
            upper = np.percentile(sorted_data, confidence + (100 - confidence) / 2)
            return lower, upper

        # Performing the bootstrap sampling and computing the bootstrap replicate 
        # of the mean together with its standard error
        bootstrap_mean, standard_error_mean, bootstrap_means = bootstrap_resampling(x_data, 
                                                                                    1000, np.mean)
        print('The sample mean computed from %s bootstrap samples: %f' % 
              (1000, bootstrap_mean))
        print('The bootstrapped estimate for the standard error of the mean:',
              standard_error_mean)

        # Computing the 95% confidence interval 
        lower, upper = compute_confidence_interval(bootstrap_means, 95)
        confidence_interval = (lower, upper)
        print('The 95% confidence interval of the mean:', confidence_interval)

        print('Overall, mean of the dataset can be reported as: %.3f +- %.3f, (%.3f, %.3f)\n' % 
             (bootstrap_mean, standard_error_mean, lower, upper))

        # Plotting an histogram for the bootstrap distribution
        plt.figure(figure_num)
        figure_num += 1
        plt.title('Histogram of the bootstrapped means')
        plt.ylabel('Counts')
        plt.xlabel('Means')
        plt.hist(bootstrap_means, bins=50, edgecolor='black', linewidth=1.2)
        plt.show(block=False)

        # PART F
        print('PART F\n')

        # Performing the bootstrap sampling and computing the bootstrap replicate of the
        # standard deviation together with its standard error
        bootstrap_std, standard_error_std, bootstrap_stds = bootstrap_resampling(x_data, 
                                                                                 1000, np.std)
        print('The sample standard deviation computed from %s bootstrap samples: %f' % 
              (1000, bootstrap_std))
        print('The bootstrapped estimate for the standard error of the standard deviation:',
              standard_error_std)

        # Computing the 95% confidence interval 
        lower, upper = compute_confidence_interval(bootstrap_stds, 95)
        confidence_interval = (lower, upper)
        print('The 95% confidence interval of the standard deviation:', confidence_interval)

        print('Overall, standard deviation of the dataset can be reported as: %.3f +- %.3f, (%.3f, %.3f)\n'
              % (bootstrap_std, standard_error_std, lower, upper))

        # Plotting an histogram for the bootstrap distribution
        plt.figure(figure_num)
        figure_num += 1
        plt.title('Histogram of the bootstrapped standard deviations')
        plt.ylabel('Counts')
        plt.xlabel('Standard deviations')
        plt.hist(bootstrap_stds, bins=50, edgecolor='black', linewidth=1.2)
        plt.show(block=False)

        # PART G
        print('PART G\n')

        # Function to perform Jacknife resampling
        def jackknife_resampling(data, stat_func):
            """
            Given the data and the statistic of interest; this function returns a
            list of statistics obtained from each jacknifed sample of the original data.
            Args:
                data: The original data
                stat_func: The function to compute the statistic of interest 
                    (e.g.: np.mean, np.std, etc.)
            Returns: 
                jackknife_replicate: The mean of all jackknife replicates
                standard_error: The standard error of the jackknife replicate
                jackknife_replicates: The list of statistics obtained from the 
                    jackknifed samples
            """
            jackknife_replicates = []
            jackknifes = np.size(data)
            for i in range(jackknifes):
                jackknife_data = [elem for j, elem in enumerate(data) if i != j]
                jackknife_replicate_i = stat_func(jackknife_data)
                jackknife_replicates.append(jackknife_replicate_i)
            return np.mean(jackknife_replicates), np.std(jackknife_replicates), jackknife_replicates

        # Performing the jackknife sampling and computing the jackknife replicate 
        # of the mean togerther with its standard error
        jackknife_mean, standard_error_mean, jackknife_means = jackknife_resampling(x_data, np.mean)
        print('The sample mean computed from jackknife samples:', jackknife_mean)
        print('The jackknifed estimate for the standard error of the mean:',
              standard_error_mean)

        # Computing the 95% confidence interval 
        lower, upper = compute_confidence_interval(jackknife_means, 95)
        confidence_interval = (lower, upper)
        print('The 95% confidence interval of the mean:', confidence_interval)

        print('Overall, mean of the dataset can be reported as: %.3f +- %.3f, (%.3f, %.3f)\n' % 
             (jackknife_mean, standard_error_mean, lower, upper))

        # Plotting an histogram for the jackknife distribution
        plt.figure(figure_num)
        figure_num += 1
        plt.title('Histogram of the jackknifed means')
        plt.ylabel('Counts')
        plt.xlabel('Means')
        plt.hist(jackknife_means, bins=5, edgecolor='black', linewidth=1.2)
        plt.show(block=False)

        # Performing the jackknife sampling and computing the jackknife replicate 
        # of the standard deviation togerther with its standard error
        jackknife_std, standard_error_std, jackknife_stds = jackknife_resampling(x_data, np.std)
        print('The sample standard deviation computed from jackknife samples:', jackknife_std)
        print('The jackknifed estimate for the standard error of the standard deviation:',
              standard_error_std)

        # Computing the 95% confidence interval 
        lower, upper = compute_confidence_interval(jackknife_stds, 95)
        confidence_interval = (lower, upper)
        print('The 95% confidence interval of the standard deviation:', confidence_interval)

        print('Overall, standard deviation of the dataset can be reported as: %.3f +- %.3f, (%.3f, %.3f)\n' % 
             (jackknife_std, standard_error_std, lower, upper))

        # Plotting an histogram for the jackknife distribution
        plt.figure(figure_num)
        figure_num += 1
        plt.title('Histogram of the jackknifed standard deviations')
        plt.ylabel('Counts')
        plt.xlabel('Standard deviation')
        plt.hist(jackknife_stds, bins=5, edgecolor='black', linewidth=1.2)
        plt.show(block=False)

        # Show all figures
        plt.show()

    elif question == '3' :
        
        # Necessary imports
        import numpy as np
        import matplotlib.pyplot as plt # for bar plots
        from scipy.special import comb # for efficient combination computation

        # QUESTION 3
        print('QUESTION 3\n')

        # PART A
        print('PART A\n')

        # Constants obtained from tasks involving language engagement
        ACTIVE_L = 103 # number of positive Broca activations
        TOTAL_L = 869 # total number of trials

        # Constants obtained from tasks not involving language engagement
        ACTIVE_NL = 199 # number of positive Broca activations
        TOTAL_NL = 2353 # total number of trials

        def likelihood_beurnoulli(prob, num_positive, total):
            """
            Likelihood function of the beurnoulli distribution.
            Args:
                prob: The probability that a binary event has a postive outcome
                num_positive: Number of positive outcomes
                total: Total number of observations/trials
            Returns:
                likelihood: The likelihood of having the beurnoulli distribution 
                    with the specified arguments
            """
            num_negative = total - num_positive
            likelihood = (prob ** num_positive) * ((1 - prob) ** num_negative)
            likelihood *= comb(total, num_positive)
            return likelihood

        x = np.arange(0, 1.001, 0.001) # probability values to try
        # Compute the likelihood vectors for language invloving tasks and others
        likelihoods_l = likelihood_beurnoulli(x, ACTIVE_L, TOTAL_L)
        likelihoods_nl = likelihood_beurnoulli(x, ACTIVE_NL, TOTAL_NL)

        # Plot likelihoods_l
        figure_num = 1
        plt.figure(figure_num)
        figure_num += 1
        plt.bar(np.arange(len(x)), likelihoods_l, color='b')
        plt.xlim(0, 200)
        plt.xticks(np.arange(0, 201, step=50), (0, 0.05, 0.1, 0.15, 0.2))
        plt.xlabel('Probability')
        plt.ylabel('Likelihood')
        plt.title('Discretized likelihood function\n for language involving tasks')
        plt.show(block=False)

        # Plot likelihoods_nl
        plt.figure(figure_num)
        figure_num += 1
        plt.bar(np.arange(len(x)), likelihoods_nl, color='r')
        plt.xlim(0, 200)
        plt.xticks(np.arange(0, 201, step=50), (0, 0.05, 0.1, 0.15, 0.2))
        plt.xlabel('Probability')
        plt.ylabel('Likelihood')
        plt.title('Discretized likelihood function\n for language excluding tasks')
        plt.show(block=False)

        # PART B
        print('PART B\n')

        x_l_max = x[np.argmax(likelihoods_l)]
        print('The probability that maximizes the discretized likelihood of the data ' +
              'obtained from the language involving tasks: %.3f, %.5f' % (x_l_max, 
              likelihood_beurnoulli(x_l_max, ACTIVE_L, TOTAL_L)))
        x_nl_max = x[np.argmax(likelihoods_nl)]
        print('The probability that maximizes the discretized likelihood of the data ' +
              'obtained from the language excluding tasks: %.3f, %.5f' % (x_nl_max, 
              likelihood_beurnoulli(x_nl_max, ACTIVE_NL, TOTAL_NL)))

        # PART C
        print('\nPART C\n')

        # Assumption is a uniform prior
        uniform_prior = 1 / len(x)
        # Marginalize the prior out in the conditional distribution to compute
        # the normalizer
        normalizer_l = np.sum(likelihoods_l * uniform_prior)
        # Apply Bayes rule
        posterior_l = likelihoods_l * uniform_prior / normalizer_l

        # Plot posterior_l
        plt.figure(figure_num)
        figure_num += 1
        plt.bar(np.arange(len(x)), posterior_l, color='g')
        plt.xlim(0, 200)
        plt.xticks(np.arange(0, 201, step=50), (0, 0.05, 0.1, 0.15, 0.2))
        plt.xlabel('x_l')
        plt.ylabel('value of posterior')
        plt.title('Discretized posterior distribution\nfor language involving tasks')
        plt.show(block=False)

        # Compute the cumulative distribution
        cdf_l = np.array([np.sum(posterior_l[:i]) for i in range(1, len(x) + 1)])

        # Plot cdf_l
        plt.figure(figure_num)
        figure_num += 1
        plt.bar(np.arange(len(x)), cdf_l, color='navy')
        plt.xticks(np.arange(len(x), step=100), 
                   (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))
        plt.xlabel('x_l')
        plt.ylabel('value of cumulative posterior')
        plt.title('Cumulative posterior distribution\nfor language involving tasks')
        plt.show(block=False)

        # Approximating the lower and higher 95% confidence bounds using the cdf
        index_lower = np.argmin(np.abs(cdf_l - 0.025))
        index_upper = np.argmin(np.abs(cdf_l - 0.975))
        print('lower and higher 95%% confidence bounds of x_l respectively: (%.3f, %.3f)' % 
              (x[index_lower], x[index_upper]))

        # Marginalize the prior out in the conditional distribution to compute
        # the normalizer
        normalizer_nl = np.sum(likelihoods_nl * uniform_prior)
        # Apply Bayes rule
        posterior_nl = likelihoods_nl * uniform_prior / normalizer_nl

        # Plot posterior_nl
        plt.figure(figure_num)
        figure_num += 1
        plt.bar(np.arange(len(x)), posterior_nl, color='brown')
        plt.xlim(0, 200)
        plt.xticks(np.arange(0, 201, step=50), (0, 0.05, 0.1, 0.15, 0.2))
        plt.xlabel('x_nl')
        plt.ylabel('value of posterior')
        plt.title('Discretized posterior distribution\nfor language excluding tasks')
        plt.show(block=False)

        # Compute the cumulative distribution
        cdf_nl = np.array([np.sum(posterior_nl[:i]) for i in range(1, len(x) + 1)])

        # Plot cdf_nl
        plt.figure(figure_num)
        figure_num += 1
        plt.bar(np.arange(len(x)), cdf_nl, color='salmon')
        plt.xticks(np.arange(len(x), step=100), 
                   (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))
        plt.xlabel('x_nl')
        plt.ylabel('value of cumulative posterior')
        plt.title('Cumulative posterior distribution\nfor language excluding tasks')
        plt.show(block=False)

        # Approximating the lower and higher 95% confidence bounds using the cdf
        index_lower = np.argmin(np.abs(cdf_nl - 0.025))
        index_upper = np.argmin(np.abs(cdf_nl - 0.975))
        print('lower and higher 95%% confidence bounds of x_nl respectively: (%.3f, %.3f)' % 
              (x[index_lower], x[index_upper]))

        # PART D
        print('\nPART D\n')

        joint_posterior = np.ma.outer(posterior_l, posterior_nl) # outer product

        plt.figure(figure_num)
        figure_num += 1
        plt.imshow(joint_posterior)
        plt.colorbar()
        plt.title('The joint posterior distribution')
        plt.xlabel('x_nl')
        plt.ylabel('x_l')
        plt.xticks(np.arange(len(x), step=100),
                   (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))
        plt.yticks(np.arange(len(x), step=100),
                   (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1))
        plt.show(block=False)

        # x_l > x_nl corresponds to the lower triangular part
        mask = np.zeros((len(x), len(x)), dtype=bool)
        mask[np.tril_indices(len(x), k=-1)] = True
        sum_x_l_greater = np.sum(joint_posterior[mask]) # masking
        print('Sum of the posterior probabilities such that x_l > x_nl: ', sum_x_l_greater)
        # x_l <= x_nl corresponds to the diagonal and upper triangular parts
        sum_x_l_less_equal = np.sum(joint_posterior[np.logical_not(mask)])
        print('Sum of the posterior probabilities such that x_l <= x_nl: ', sum_x_l_less_equal)

        # PART E
        print('\nPART E\n')

        PROB_L = 0.5 # probability of language involvement
        prob_nl = 1 - PROB_L
        prob_active = x_l_max * PROB_L + x_nl_max * prob_nl # additivity axiom 
        # Apply Bayes Rule
        prob_l_given_active = x_l_max * PROB_L / prob_active
        print('P(language|activation) is computed as: ', prob_l_given_active)

        # Show all figures
        plt.show()

efe_acer_21602217_hw1(question)